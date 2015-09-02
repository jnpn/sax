'''
Generator based XML tokenizer (SAX like)
'''

import io

xml = '/home/agumonkey/code/embauches/grammarize/tree.xml'

def peek(stream, forward=1, span=0):
    '''
    >>> bs = io.BytesIO(b'aBcDeF')
    >>> peek(bs, forward=2)
    b'B'
    >>> peek(bs, forward=2)
    b'B'
    >>> peek(bs, forward=2, span=2)
    b'BcD' # BUG
    '''
    print('[TODO] fix bug in peek, see docstring.')
    p = stream.tell()
    c = stream.read(forward+span)[span-1:] # python can be weird...
    stream.seek(p)
    return c

def root(s):
    c1 = peek(s)
    if c1 == b'<':
        c2 = peek(s, 2)
        if c2 == b'?':
            yield from inst(s)
        elif c2 == b'/':
            yield from etag(s)
        else:
            yield from otag(s)
    elif c1 == b'':
        raise StopIteration # EOF
    else:
        yield from text(s)
        s.seek(s.tell() - 1)

def otag(s):
    '''
    WARNING inclusive limit '>' marks the end, MUST be added outside the loop
    '''
    c = s.read(1)
    a = b''
    while c != b'>' and c != b'':
        a += c
        c = s.read(1)
    yield ('otag', a + b'>') if c != b'' else ('error', a)
    yield from root(s)

def etag(s):
    '''
    WARNING inclusive limit '>' marks the end, MUST be added outside the loop
    '''
    c = s.read(1)
    a = b''
    while c != b'>' and c != b'':
        a += c
        c = s.read(1)
    yield ('etag', a + b'>') if c != b'' else ('error', a)
    yield from root(s)

def inst(s):
    '''
    WARNING inclusive limit '>' marks the end, MUST be added outside the loop
    '''
    c = s.read(1)
    a = b''
    while c != b'>' and c != b'':
        a += c
        c = s.read(1)
    yield ('inst', a + b'>') if c != b'' else ('error', a)
    yield from root(s)

def text(s):
    c = s.read(1)
    a = b''
    while c != b'<' and c != b'':
        a += c
        c = s.read(1)
    yield ('text', a) # if c != b'' else ('error', a)
    if c != b'':
        s.seek(s.tell() - 1) # Finally... still ugly code
    yield from root(s)
