# Trains to categorize articles into groups using keywords

from nltk.corpus import stopwords

stops = stopwords.words('english')

def remove_keywords(s):
    return [w.strip() for w in s.split('\s+') if w not in stops]

def bag_words(kws):
    bag = {}
    for w in kws:
        if w not in bag:
            bag[w] = 0
        bag[w] += 1
    return bag
