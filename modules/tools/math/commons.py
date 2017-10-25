from collections import Counter

def reduce(fn, lst, acc=None):
    if not acc:
        acc = lst[0]
        lst = lst[1:]
    for l in lst:
        acc = fn(acc, l)
    return acc

def stddev(data):
    N = len(data)
    mean = sum(data)/N
    return mean, (sum([((mean-n) ** 2) for n in data]))/N

def normalize(max_, data):
    dmax, dmin = max(data), min(data)
    rng = dmax - dmin
    if rng == 0:
        return data
    return [(n/rng) * max_ for n in data]

def truncate(n, acc):
    return int(n * (10 ** acc)) / (10 ** acc)

def collect(lst):
    return Counter(lst)

def intersect(*dicts):
    return reduce(lambda acc, n: acc & n, dicts)
