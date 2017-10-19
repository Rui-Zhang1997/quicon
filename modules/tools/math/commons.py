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
