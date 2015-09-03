'''
Classic imperative attempt
'''


class UknownToken(Exception):
    pass


def log(f):
    def _(*p, **k):
        r = f(*p, **k)
        print(f.__name__, '->', r)
        return r
    return _


@log
def peek(stream, off=1):
    p = stream.tell()
    c = stream.read(off)[-1:]
    stream.seek(p)
    return c


def testpeek0():
    c = peek(io.StringIO('<foo>'), off=2)
    e = 'f'
    return c == e


def testpeek1():
    c = peek(io.StringIO('<foo>'), off=3)
    e = 'o'
    return c == e


def tok(stream):
    import pdb; pdb.set_trace()

    c = peek(stream)
    while c != '':
        k = None
        if c == '<':                             # * TAG
            cc = peek(stream, off=2)
            if cc == '?':
                k = 'instruction'                # INSTRUCTION TAG
            elif cc == '/':
                k = 'closing'                    # CLOSING TAG
            elif cc == '!':
                ccc = peek(stream, off=3)
                if ccc == '-':
                    k = 'comment'                # COMMENT TAG
                elif ccc == 'D':
                    k = 'doctype'                # DOCTYPE TAG
                else:
                    raise UknownToken(c+cc+ccc)
            else:
                k = 'opening'                    # OPEN TAG

            # TAG work here
            acc = ''
            tac = stream.read(1)
            print(tac, acc)
            while tac != '>':
                acc += tac
                tac = stream.read(1)

            # hold on, self closing ?
            if acc[-1] == '/':
                k = 'selfclosing'                # SELFCLOSING

            acc += '>'
            yield k, acc

        else:                                    # TEXT
            k = 'text'
            acc = ''
            tec = stream.read(1)
            while tec != '<' and tec != '':
                acc += tec
                tec = stream.read(1)

            if peek(stream) != '':
                stream.seek(stream.tell() - 1)  # must rewind before '<'
                # only if not at the end.
            yield k, tec


def test():
    import io
    return list(tok(io.StringIO('<foo>')))


def sax_inst(stream):
    """
    Docstrings are
    weird.
    """
    c = stream.read(1)
    inst = c
    while c != '?':
        inst += c
        c = stream.read(1)
    q = stream.read(1)
    b = stream.read(1)
    return inst + q + b

def sax_otag(stream): pass
def sax_ctag(stream): pass
def sax_text(stream): pass
