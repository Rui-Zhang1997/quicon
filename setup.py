from modules.tools.classifier import classifier as cls
from modules.db import polydb as pdb
from modules.tools.scraper import scraper as ssc
from modules.tools.scraper import text_scraper as tsc
# from modules.models import models

# pdb.init()
def stat():
    c, l = cls.get_stats_sources()
    print(c,l)

def scrape():
    ssc.run_scraper(ssc.lib_subreddits, models.Liberal)
    ssc.run_scraper(ssc.cons_subreddits, models.Conservative)

stat()
