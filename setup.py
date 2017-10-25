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

tscrape('https://www.washingtonpost.com/news/post-politics/wp/2017/10/25/trump-punches-back-at-flake-and-corker-claims-a-love-fest-of-support-in-senate/?hpid=hp_hp-top-table-main_pp-trump-837am%3Ahomepage%2Fstory&utm_term=.9f192f693848https://www.washingtonpost.com/news/post-politics/wp/2017/10/25/trump-punches-back-at-flake-and-corker-claims-a-love-fest-of-support-in-senate/?hpid=hp_hp-top-table-main_pp-trump-837am%3Ahomepage%2Fstory&utm_term=.9f192f693848')
