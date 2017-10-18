'''
Attempts to pull the article from news sites.
'''

from bs4 import BeautifulSoup as bsoup
import requests as req

'''
Attempts to grab the proper section.
Must take into account:
    1. Number of paragraph tags in div
    2. Length of each paragraph tag (how many words)
    3. Total number of words contained in the tag
'''
def find_text(text_groups):
    group_sizes = dict([(tag, len(text_groups[tag])) for tag in text_groups])
    keys = [tag for tag in text_groups]
    pass

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
