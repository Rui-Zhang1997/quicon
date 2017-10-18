import praw
import os
import yaml
import sys
import re
import time
from modules.models import models
from modules.db import polydb as pd
from modules.db import polyorm as orm
from sqlalchemy.inspection import inspect
from sqlalchemy.sql import text

CONF_FILE = 'config.yaml'
config = None

# reading in config file
try:
    with open(CONF_FILE) as conf:
        config = yaml.load(conf)
except FileNotFoundError as e:
    print(e)
    print("Please ensure that %s is located in the root of this project" % CONF_FILE)
    sys.exit(1)

reddit = praw.Reddit(client_id=config['client_id'],
                     client_secret=config['client_secret'],
                     password=config['password'],
                     user_agent=config['user_agent'],
                     username=config['username'])

subreddits = [
    'worldnews',
    'news',
    'neutralnews',
    'worldpolitics',
    'worldevents',
    'uspolitics',
    'liberal',
    'conservative',
    'the_donald'

]

def scrape_subreddits(sr):
    return reddit.subreddit(sr).hot(limit=25)

def insert_to_table(table, objs, update_keys):
    session = pd.get_session()
    insert_query = orm.Insert(table)
    insert_query.set_update_fields(update_keys)
    if len(objs) == 0:
        return
    insert_query.set_fields(objs[0].keys())
    for obj in objs:
        insert_query.add_values(obj.values())
    session.execute(text(insert_query.gq()))
    session.commit()

def scrape_all_comments(cfs):
    comments = []
    for cf in cfs:
        for comment in cf.list():
            if isinstance(comment, praw.models.Comment):
                _id = comment.id
                parent = comment.parent().id
                content = ' '.join(re.split('\s+', re.sub('[^a-zA-Z0-9-_ ]', ' ', comment.body))).lower()
                subreddit = comment.subreddit.display_name
                upvotes = comment.ups
                author = comment.author.name if comment.author else ''
                time = comment.created
                cmt = models.Comment(_id, parent, subreddit, upvotes, author, content, time)
                comments.append(cmt)
        insert_to_table('comments', comments, {'content': 'content'})

def scrape_all_posts(submissions):
    posts = []
    cfs = []
    for submission in submissions:
        _id = submission.id
        title = ' '.join(re.split('\s+', re.sub('[^a-zA-Z0-9-_ ]', ' ', submission.title))).lower()
        print('Submission: %s' % title)
        author = submission.author.name if submission.author else ''
        upvotes = submission.ups
        timePosted = submission.created
        subreddit = submission.subreddit.display_name
        source = submission.url
        scrape_all_comments([submission.comments])
        sub = models.Submission(_id, subreddit, title, author, source, upvotes, timePosted)
        posts.append(sub)
    insert_to_table('submissions', posts, {'title': 'title'})

def run_scraper():
    for sr in subreddits:
        stime = int(time.time() * 1000)
        print("Running scrape on subreddit: %s" % sr)
        scrape_all_posts(scrape_subreddits(sr))
        print("Finished scraping subreddit: %s. Completed in %d ms." % (sr, int(time.time() * 1000) - stime))
