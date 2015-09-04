'''
Generator based XML tokenizer (SAX like)
'''

from sax.tokenizer.exceptions import UnknownElement
from sax.prelude import peek
from sax.tokenizer.interface import comment, doctype, opening, \
    closing, selfclosing, instruction, text, error


def tok(s):
    p = s.tell()
    while peek(s) != '':
        c1 = peek(s)
        if c1 == '<':
            c2 = peek(s, 2)
            if c2 == '?':
                yield from instruction_tokenizer(s)
            elif c2 == '!':
                c3 = peek(s, 3)
                if c3 == '-':
                    yield from comment_tokenizer(s)
                elif c3 in {'d', 'D'}:
                    yield from doctype_tokenizer(s)
                else:
                    raise UnknownElement(s)
            elif c2 == '/':
                yield from closing_tokenizer(s)
            else:
                yield from opening_tokenizer(s)
        elif c1 == '':
            raise StopIteration  # EOF
        else:
            yield from text_tokenizer(s)
        assert s.tell() > p, "%d should be larger than %d" % (s.tell(), p)


def comment_tokenizer(s):
    c = s.read(1)
    a = ''
    while c != '>' and c != '':
        a += c
        c = s.read(1)
    yield (comment, a + '>') if c != '' else ('error', a)


def doctype_tokenizer(s):
    c = s.read(1)
    a = ''
    while c != '>' and c != '':
        a += c
        c = s.read(1)
    yield (doctype, a + '>') if c != '' else ('error', a)


def opening_tokenizer(s):
    '''
    WARNING inclusive limit '>' marks the end, MUST be added outside the loop
    '''
    c = s.read(1)
    a = ''
    is_selfclosing = False
    while c != '>' and c != '':
        a += c
        c = s.read(1)

    if c == '>' and a[-1] == '/':
        is_selfclosing = True

    if is_selfclosing:
        yield (selfclosing, a + '>')  # reuse the whole 'text' to allow checks
    else:
        yield (opening, a + '>') if c != '' else (error, a)


def closing_tokenizer(s):
    '''
    WARNING inclusive limit '>' marks the end, MUST be added outside the loop
    '''
    c = s.read(1)
    a = ''
    while c != '>' and c != '':
        a += c
        c = s.read(1)
    yield (closing, a + '>') if c != '' else (error, a)


def instruction_tokenizer(s):
    '''
    WARNING inclusive limit '>' marks the end, MUST be added outside the loop
    '''
    c = s.read(1)
    a = ''
    while c != '>' and c != '':
        a += c
        c = s.read(1)
    yield (instruction, a + '>') if c != '' else (error, a)


def text_tokenizer(s):
    c = s.read(1)
    a = ''
    while c != '<' and c != '':
        a += c
        c = s.read(1)
    yield (text, a)  # if c != '' else (error, a)
    if c != '':
        s.seek(s.tell() - 1)  # Finally... still ugly code
