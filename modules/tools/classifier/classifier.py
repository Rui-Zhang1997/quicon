'''
This is the meat of the project. The goal is to pull news stories from a number of subreddits,
analyze the contents of the comments, analyze the general sentiment of the article, its users,
political leaning, etc. It will hopefully be able to tell us a few things:
    1. What are the most popular topics for those subreddits
    2. Are comments usually LRoC?
    3. Are their more upvotes or downvotes on comments that are LRaC
    4. Who are more active on reddit in general, LRoC?
    5. What are the leaning of the sources used, LRoC?

Method - Primitive:
    For each subreddit, we pull the top 20 hottest posts of that present time, as well
    as 10 random posts from the top 100, and gather a few pieces of data:
        1. Source
        2. Title
        3. Who commented
        4. Do the people who comments post on political subreddits with what leaning
        5. Are the reactions to their posts negative or positive
    From this we can gather some information regarding what people are feeling and
    who visits those subreddits.

This kind of builds off of Max Candocia's work.
'''

'''
Gets sources and classifies them as conservative, liberal, or moderate.
Takes the sources from the database and sorts them in three groups:
Strictly Conservative: Only used in conservative subreddits
Strictly Liberal: Only used in liberal subreddits
Moderate: Appears in both subreddits
'''
from modules.tools.math import commons as cms
from modules.models import models
from modules.tools.scraper import text_scraper as tsc
from modules.tools.math import commons as cms
import math

def enforce_threshhold(d, t):
    return dict([(k, d[k]) for k in list(filter(lambda k: d[k] > t, d))])

def get_stats_sources():
    cons_sources, lib_sources = tsc.get_sources_from_table(models.Conservative), tsc.get_sources_from_table(models.Liberal)
    cons_freq, lib_freq = enforce_threshhold(cms.collect(list(cons_sources)), 2), enforce_threshhold(cms.collect(list(lib_sources)), 2)
    return cons_freq, lib_freq

def normalize_data(freqs):
    mean, variance = cms.variance([freqs[k] for k in freqs])
    stddev = math.sqrt(variance)
    for k,v in freqs.items():
        freqs[k] = (v-mean)/stddev

'''
Z-scores of the data. Can now make assumptions.
TODO: Factor in temporal ratings data (though there
is the chance that upvote ratio will not be significantly
affected by time)
'''
def normalize_for_groups(cons_freq, lib_freq):
    cons_keyset = set(cons_freq)
    libs_keyset = set(lib_freq)
    common_keys = cons_keyset & libs_keyset
    common_freqs = dict([(k, cons_freq[k] - lib_freq[k]) for k in common_keys])
    return normalize_data(cons_freq), normalize_data(lib_freq), normalize_data(common_freqs)
