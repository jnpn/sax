'''
Generator based XML tokenizer (SAX like)
'''



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

class UnknownElement(Exception): pass

def tok(s):
    c1 = peek(s)
    if c1 == '<':
        c2 = peek(s, 2)
        if c2 == '?':
            yield from instruction(s)
        elif c2 == '!':
            c3 = peek(s, 3)
            if c3 == '-':
                yield from comment(s)
            elif c3 == 'D':
                yield from doctype(s)
            else:
                raise UnknownElement(s)
        elif c2 == '/':
            yield from closing(s)
        else:
            yield from opening(s)
    elif c1 == '':
        raise StopIteration  # EOF
    else:
        yield from text(s)
        s.seek(s.tell() - 1)


def comment(s):
    c = s.read(1)
    a = ''
    while c != '>' and c != '':
        a += c
        c = s.read(1)
    yield ('comment', a + '>') if c != '' else ('error', a)
    yield from tok(s)


def doctype(s):
    c = s.read(1)
    a = ''
    while c != '>' and c != '':
        a += c
        c = s.read(1)
    yield ('doctype', a + '>') if c != '' else ('error', a)
    yield from tok(s)


def opening(s):
    '''
    WARNING inclusive limit '>' marks the end, MUST be added outside the loop
    '''
    c = s.read(1)
    a = ''
    selfclosing = False
    while c != '>' and c != '':
        a += c
        c = s.read(1)

    if c == '>' and a[-1:] == '/':
        selfclosing = True

    yield ('opening', a + '>') if c != '' else ('error', a)
    if selfclosing:
        yield ('closing', a + '>')  # reuse the whole 'text' to allow checks
    yield from tok(s)

def closing(s):
    '''
    WARNING inclusive limit '>' marks the end, MUST be added outside the loop
    '''
    c = s.read(1)
    a = ''
    while c != '>' and c != '':
        a += c
        c = s.read(1)
    yield ('closing', a + '>') if c != '' else ('error', a)
    yield from tok(s)

def instruction(s):
    '''
    WARNING inclusive limit '>' marks the end, MUST be added outside the loop
    '''
    c = s.read(1)
    a = ''
    while c != '>' and c != '':
        a += c
        c = s.read(1)
    yield ('instruction', a + '>') if c != '' else ('error', a)
    yield from tok(s)

def text(s):
    c = s.read(1)
    a = ''
    while c != '<' and c != '':
        a += c
        c = s.read(1)
    yield ('text', a)  # if c != '' else ('error', a)
    if c != '':
        s.seek(s.tell() - 1)  # Finally... still ugly code
    yield from tok(s)
