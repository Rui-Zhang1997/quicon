# from modules.tools.classifier import classifier as cls
# from modules.db import polydb as pdb
from modules.tools.scraper import scraper as ssc
from modules.tools.scraper import text_scraper as tsc
# from modules.models import models

# pdb.init()
def stat():
    c, l = cls.get_stats_sources()
    print(cls.normalize_for_groups(c,l))

def scrape():
    ssc.run_scraper(ssc.lib_subreddits, models.Liberal)
    ssc.run_scraper(ssc.cons_subreddits, models.Conservative)

def tscrape(url):
    print(tsc.scrape_article(url))

tscrape('http://www.reuters.com/article/us-usa-trump-russia-charges/first-charges-filed-in-u-s-special-counsels-russia-investigation-source-idUSKBN1CX00V')
