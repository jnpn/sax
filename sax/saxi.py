'''
Classic imperative attempt
'''


class UknownToken(Exception):
    pass


def peek(stream, off=1):
    p = stream.tell()
    c = stream.read(off)[-1:]
    stream.seek(p)
    return c


def tok(stream):

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
            yield k, acc

        c = peek(stream)
def sax_otag(stream): pass
def sax_ctag(stream): pass
def sax_text(stream): pass
