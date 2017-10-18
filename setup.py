from modules.tools.classifier import classifier
from modules.tools.scraper import text_scraper as tsc
from modules.db import polydb as db

db.init()

ps = tsc.extract_article('http://www.cbc.ca/news/canada/montreal/bill-62-stephanie-vallee-muslim-niqab-1.4356263')
print(ps)
