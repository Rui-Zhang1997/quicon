'''
Attempts to pull the article from news sites.
'''

from bs4 import BeautifulSoup as bsoup
import requests as req
from modules.tools.math import commons as mathcms
from modules.db import polydb as pd
from nltk.corpus import stopwords
import re

STOPS = stopwords.words('english')

def clean_up(text):
    return [re.sub('[^a-zA-Z]', ' ', w).lower().strip() for w in re.split('\s+', text) if re.sub('[^a-zA-Z0-9]', ' ', w).lower().strip() not in STOPS]

def bag_words(text, sort_max=True):
    words = clean_up(text)
    bow = {}
    for word in words:
        if word == '':
            continue
        bow[word] = bow[word] + 1 if word in bow else 1
    if sort_max:
        bow = sorted([(k, v) for k, v in bow.items()], key=lambda n: n[1])
    return bow

'''
Attempts to grab the proper section.
Must take into account:
    1. Number of paragraph tags in div
    2. Length of each paragraph tag (how many words)
    3. Total number of words contained in the tag
    4. Phrase Frequency
'''
def find_text(text_groups):
    group_sizes = dict([(tag, len(text_groups[tag])) for tag in text_groups])
    keys = [tag for tag in text_groups]
    paragraph_sizes = {}
    for key in text_groups:
        paragraph_sizes[key] = [len(s) for s in text_groups[key]]
        paragraph_sizes[key] = mathcms.normalize(10, paragraph_sizes[key])
    std_devs = dict([(tag, mathcms.stddev(v)) for tag, v in paragraph_sizes.items()])
    for k, v in std_devs.items():
        std_devs[k] = (mathcms.truncate(v[0], 3), mathcms.truncate(v[1], 3))
    difference = -1
    text_tag = ''
    for tag, (mean, variance) in std_devs.items():
        if (abs(mean - variance) < difference) or (difference == -1):
            difference = abs(mean - variance)
            text_tag = tag
    return ' '.join(text_groups[text_tag])

def extract_article(url):
    r = req.get(url)
    soup = bsoup(r.text, 'html.parser')
    texts = soup.find_all('p')
    text_groups = {}
    for t in texts:
        parent = t.parent
        while parent and parent.name != 'div' and parent.name != 'body':
            parent = parent.parent
        parent_id = parent['id'] if parent.has_attr('id') else (parent['class'] if parent.has_attr('class') else parent.name)
        if isinstance(parent_id, list):
            parent_id = ':'.join(parent_id)
        if parent_id not in text_groups:
            text_groups[parent_id] = []
        text_groups[parent_id].append(t.text.strip())
    return find_text(text_groups)

def get_sources_from_table(Table, strip_www=True):
    session = pd.get_session()
    sources = []
    for source in session.query(Table.source):
        src = re.split('/+', source[0])[1]
        if strip_www:
            src = src.replace('www.', '')
        sources.append(src)
    return sources
