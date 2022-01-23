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
    '''
    Stateless look at a stream.
    Read <off> element(s), restore stream pos, returns the last element.
    '''
    p = stream.tell()
    c = stream.read(off)[-1:]
    stream.seek(p)
    return c


# def peek(stream, off=1, span=0):
#     '''
#     Extension of the above to return <span> element(s)
#     '''
#     # print('[TODO] fix bug in peek, see docstring.')
#     p = stream.tell()
#     c = stream.read(off + span)[span - 1:]  # python can be weird...
#     stream.seek(p)
#     return c

def logged(f):
    fn_name = f.__name__
    def _(*ks,**kw):
        print(f'[log.{fn_name}]', ks, kw, end='')
        v = f(*ks, **kw)
        print('->',v)
        return v
    return _
