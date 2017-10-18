import os, sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
class Submission(Base):
    __tablename__ = 'submissions'
    id = Column(String(10), primary_key=True)
    subreddit = Column(String(200))
    title = Column(String(1000))
    author = Column(String(200))
    upvotes = Column(Integer)
    timePosted = Column(Float)
    source = Column(String(225))
    def __init__(self, _id, subreddit='', title='', author='', source='', upvotes=0, timePosted=0):
        self.id = _id
        self.subreddit = subreddit
        self.author = author
        self.upvotes = upvotes
        self.title = title
        self.timePosted = timePosted
        self.source = source

    def keys(self):
        return ['id', 'subreddit', 'title', 'author', 'upvotes', 'timePosted', 'source']

    def values(self):
        return [self.id, self.subreddit, self.title, self.author, self.upvotes, self.timePosted, self.source]

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(String(10), primary_key=True)
    parent_id = Column(String(10), primary_key=True)
    subreddit = Column(String(125))
    upvotes = Column(Integer)
    author = Column(String(200))
    content = Column(String(15000))
    timePosted = Column(Float)
    def __init__(self, _id, parent_id, subreddit='', upvotes=0, author='', content='', time=0):
        self.id = _id
        self.parent_id = parent_id
        self.subreddit = subreddit
        self.upvotes = upvotes
        self.author = author
        self.content = content
        self.timePosted = time
    
    def keys(self):
        return ['id', 'parent_id', 'subreddit', 'upvotes', 'author', 'content', 'timePosted']

    def values(self):
        return [self.id, self.parent_id, self.subreddit, self.upvotes, self.author, self.content, self.timePosted]
    
def load_to_engine(engine):
    print("Loading to engine")
    print(engine)
    Base.metadata.create_all(engine)
