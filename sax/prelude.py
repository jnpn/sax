'''
Prelude.
'''


def log(f):
    def _(*p, **k):
        r = f(*p, **k)
        print(f.__name__, '->', r)
        return r
    return _


def peek(stream, off=1):
    p = stream.tell()
    c = stream.read(off)[-1:]
    stream.seek(p)
    return c


def peek(stream, forward=1, span=0):
    '''
    >>> bs = io.StringIO('aBcDeF')
    >>> peek(bs, forward=2)
    'B'
    >>> peek(bs, forward=2)
    'B'
    >>> peek(bs, forward=2, span=2)
    'BcD'  # BUG
    '''
    # print('[TODO] fix bug in peek, see docstring.')
    p = stream.tell()
    c = stream.read(forward+span)[span-1:]  # python can be weird...
    stream.seek(p)
    return c
