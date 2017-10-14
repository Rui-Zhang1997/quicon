import praw
import os
import yaml
import sys

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
