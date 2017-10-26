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

tscrape('https://www.nytimes.com/2017/10/24/us/puerto-rico-schools.html?rref=collection%2Fsectioncollection%2Fus&action=click&contentCollection=us&region=rank&module=package&version=highlights&contentPlacement=1&pgtype=sectionfront')
