import praw
import os
import yaml
import sys
import re
from modules.models import models

CONF_FILE = 'config.yaml'
config = None

# reading in config file
try:
    with open(CONF_FILE) as conf:
        config = yaml.load(conf)
except FileNotFoundError as e:
    print(e)
    print("Please ensure that %s is located in the root of this project" % CONF_FILE)
    M
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
    'qualitynews',
    'worldevents',
    'geopolitics'
]

def scrape_subreddits(sr):
    return reddit.subreddit(sr).hot(limit=75)

def insert_to_db(db, keys, values):
    sql_query = 'INSERT INTO %s %s VALUES %s' % (db, keys, values)
    return sql_query

def insert_to_database(db, obj):
    keys, values = [], []
    for k,v in obj.__dict__.items():
        if v == None:
            continue
        keys.append(k)
        values.append('"%s"' % v if isinstance(v, str) else str(v))
    keys_str = '(' + ', '.join(keys) + ')'
    values_str = '(' + ', '.join(values) + ')'
    print(insert_to_db(db, keys_str, values_str))

def scrape_all_comments(cf):
    comments = []
    for comment in cf.list():
        if isinstance(comment, praw.models.Comment):
            _id = comment.id
            content = ' '.join(re.split('\s+', comment.body))
            subreddit = comment.subreddit.display_name
            downvotes = comment.downs
            upvotes = comment.ups
            author = comment.author.name if comment.author else ''
            time = comment.created
            parent = comment.parent_id
            cmt = models.Comment(_id, subreddit, parent, upvotes, downvotes, author, content, time)
            insert_to_database('comments', cmt)
    return comments

def scrape_all_posts(submissions):
    posts = []
    for submission in submissions:
        _id = submission.id
        title = ' '.join(re.split('\s+', submission.title))
        author = submission.author.name if submission.author else ''
        upvotes = submission.ups
        downvotes = submission.downs
        timePosted = submission.created
        subreddit = submission.subreddit.display_name
        scrape_all_comments(submission.comments)
        sub = models.Submission(_id, subreddit, title, author, upvotes, downvotes, timePosted)
        insert_to_database('submissions', sub)
    return posts

for sr in subreddits:
    scrape_all_posts(scrape_subreddits(sr))
