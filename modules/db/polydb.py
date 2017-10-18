import os
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.models import models

CONF_FILE = 'config.yaml'
config = None
sql_engine = None
sql_session = None
try:
    with open(CONF_FILE) as conf:
        config = yaml.load(conf)
except FileNotFoundError as e:
    print(e)
    print('Please ensure that config file exists at project root')

def init_db():
    print("Initializing database")
    dbc = config['db']
    global sql_engine
    sql_engine = create_engine('mysql+pymysql://%s:%s@localhost:%d/%s?charset=utf8' % (dbc['user'], dbc['pswd'], dbc['port'], dbc['name']), echo=False)
    print("Initialized database")

def init_tables():
    if sql_engine:
        print("Creating tables")
        models.load_to_engine(sql_engine)
        print("Created tables")

def init():
    init_db()
    init_tables()
    global sql_session
    sql_session = sessionmaker(bind=sql_engine)

def get_session():
    return sql_session()
