'''
Attempts to pull the article from news sites.
'''

from bs4 import BeautifulSoup as bsoup
import requests as req
from modules.tools.math import commons as mathcms
from modules.db import polydb as pd
from nltk.corpus import stopwords
from numpy import std, mean
import re

STOPS = stopwords.words('english')

'''
@param text must be aray of words
'''
def clean_up(text):
    text_list = text if isinstance(text, list) else re.split('\s+', text) # splits sentences up by whitespace
    text_list = re.split('\s+', re.sub('[^a-zA-Z0-9]', ' ', ' '.join(text_list))) # 
    return [w.lower() for w in text_list if w != '' and w.lower() not in STOPS]

def sanitize(text_groups):
    sanitized = {}
    for k,v in text_groups.items():
        sanitized[k] = [re.sub('[^a-zA-Z0-9]', ' ', p).lower().strip() for p in v] # all nonealphanumeric characters are replaced with space
        sanitized[k] = [p for p in sanitized[k] if p != ''] # only keep paragraphs that have content
    sanitized = dict([(k,v) for k,v in sanitized.items() if len(v) > 0])
    return sanitized
'''
@param text must be aray of words
'''
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
Returns common phrases.
@param text must be an array of words
@param N smallest phrase length
@param M largest phrase length
@min_occur only report phrases that occur at least min_occur times
'''
def Ngram(list_text, N=1, M=None, min_occur=2):
    if M == None:
        M = N
    grams = {}
    for i in range(N, M+1):
        for j in range(len(list_text)-i+1):
            phrase = ' '.join(list_text[j:j+i])
            grams[phrase] = grams[phrase] + 1 if phrase in grams else 1
    if min_occur > 0:
        return dict([(k, v) for k, v in grams.items() if v >= min_occur])
    return grams

'''
Gets the frequency of words and phrases between paragraphs (Hypothesis: Paragraphs in an article should have more words in common
                                                            with higher counts. T-tests of word frequencies should also indicate
                                                            whether the paragraphs are related, and article paragraphs should.)
'''
def get_freqs(text_groups):
    freqs = {}
    for k, v in text_groups.items():
        freq = {}
        freqs[k] = Ngram(re.split('\s+', ' '.join(v)), 1, 5)
    return freqs

'''
Gets the mean and standard deviation of kv-pair (Hypothesis: The lengths of paragraphs in an article should
                                                 be relatively uniform, with a higher average word count and low standard deviation)
'''
def get_stddev(text_groups):
    text_stddevs = {}
    for k, v in text_groups.items():
        sizes = [len(p) for p in v]
        text_stddevs[k] = (mean(sizes), std(sizes))
    return text_stddevs

'''
Counts the total number of words in kv-pair (Hypothesis: Articles usually contain more words than ads and redirects)
'''
def get_lengths(text_groups):
    text_lengths = {}
    for k, v in text_groups.items():
        text_lengths[k] = len(re.split('\s+', ' '.join(v)))
    return text_lengths

'''
Uses above four functions to guess what piece of text is the actual article. text_groups should ONLY contain values that are
an array of paragraphs, each cleaned for unwanted characters (replaced with spaces), all words shrunk to lowercase, and removed
paragraphs of length 0
'''
def guess_article(text_groups):
    freqs, stddev, lengths = get_freqs(text_groups), get_stddev(text_groups), get_lengths(text_groups)
    stddev_list = [(k, (m, s)) for k, (m, s) in stddev.items()]
    top_means = dict(list(reversed(sorted(stddev_list, key=lambda n: n[1][0])))[:3])
    top_devs = dict(list(reversed(sorted(stddev_list, key=lambda n: n[1][1])))[:3])
    top_lengths = dict(list(reversed(sorted([(k, l) for k, l in lengths.items()], key=lambda n: n[1])))[:3])
    common_keys = set(top_means) & set(top_devs) & set(top_lengths)
    print("COMMON_KEYS", common_keys)
    if len(common_keys) > 0:
        if len(common_keys) == 1:
            div = list(common_keys)[0]
            return div, text_groups[div]
        else: # returns the text with the longest text
            keys = list(common_keys)
            key = None
            max_ = 0
            for k in keys:
                if top_lengths[k] > max_:
                    max_ = top_lengths[k]
                    key = k
            return key, text_groups[key]
    keys = list(top_lengths)
    key = None
    max_ = 0
    for k in keys:
        if top_lengths[k] > max_:
            max_ = top_lengths[k]
            key = k
    if not key:
        print(text_groups)
        return None, None
    return key, text_groups[key]

def scrape_article(url):
    print(url)
    r = req.get(url, headers={'User-Agent': 'Polydata'})
    soup = bsoup(r.text, 'html.parser')
    texts = soup.find_all('p')
    text_groups = {}
    for t in texts:
        parent = t.parent
        while parent and parent.name not in {'div', 'body', 'article', 'section'}:
            parent = parent.parent
        if not parent:
            parent = t
        parent_id = parent['id'] if parent.has_attr('id') else (parent['class'] if parent.has_attr('class') else parent.name)
        if isinstance(parent_id, list):
            parent_id = ':'.join(parent_id)
        if parent_id not in text_groups:
            text_groups[parent_id] = []
        text_groups[parent_id].append(t.text.strip())
    return guess_article(sanitize(text_groups))

def get_sources_from_table(Table, strip_www=True):
    session = pd.get_session()
    sources = []
    for source in session.query(Table.source):
        src = re.split('/+', source[0])[1]
        if strip_www:
            src = src.replace('www.', '')
        sources.append(src)
    return sources
