'''
Prelude.
'''


def log(f):
    def _(*p, **k):
        r = f(*p, **k)
        print(f.__name__, '->', r)
        return r
    return _
