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

'''
@param text must be aray of words
'''
def clean_up(text):
    text_list = text if isinstance(text, list) else re.split('\s+', text)
    return [re.sub('[^a-zA-Z]', ' ', w).lower().strip() for w in text_list
            if re.sub('[^a-zA-Z0-9]', ' ', w).lower().strip() not in STOPS]

'''
@param text must be aray of words
'''
def bag_words(text, sort_max=True):
    print("TEXT", text)
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
Returns common phrases.
@param text must be an array of words
'''
def Ngram(text, N=1, M=None, min_occur=2):
    if M == None:
        M = N
    text = clean_up(text)
    grams = {}
    for i in range(N, M+1):
        for j in range(len(text)-i+1):
            phrase = ' '.join(text[j:j+i])
            grams[phrase] = grams[phrase] + 1 if phrase in grams else 1
    if min_occur > 0:
        return dict([(k, v) for k, v in grams.items() if v >= min_occur])
    return grams
'''
Extract text using relative sizes.
'''
def extract_article_relative_size(text_groups):
    words = {}
    for k,v in text_groups.items():
        words[k] = clean_up(' '.join(v))
'''
Extract text using N-gram frequencies
'''
def extract_article_relative_phrases(estimated_article, text_groups):
    est_gram = Ngram(estimated_article, 1, 5)
    text_grams = {}
    for key, text in text_groups.items():
        print("KEY", key)
        text_grams[key] = Ngram(' '.join(text).split(' '), 1, 5)
    print("ESTIMATED", est_gram)
    print("----------------------------------------------------")
    for k,v in text_grams.items():
        print(k,v)
        print()

def scrape_article(url):
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
    extract_article_relative_size(text_groups)
    # return extract_article_relative_phrases(extract_article_relative_size(text_groups)[1], text_groups)

def get_sources_from_table(Table, strip_www=True):
    session = pd.get_session()
    sources = []
    for source in session.query(Table.source):
        src = re.split('/+', source[0])[1]
        if strip_www:
            src = src.replace('www.', '')
        sources.append(src)
    return sources
