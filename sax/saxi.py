'''
Classic imperative attempt
'''

from collections import OrderedDict


class UknownToken(Exception):
    pass


def peek(stream, off=1):
    p = stream.tell()
    c = stream.read(off)[-1:]
    stream.seek(p)
    return c


def like(stream, string):
    assert len(string) > 0
    p = stream.tell()
    b = stream.read(len(string)) == string
    stream.seek(p)
    return b


def tok(stream):

    while peek(stream) != '':
        rules = OrderedDict([
            ('<!--', 'comment'),    # COMMENT TAG
            ('<!', 'doctype'),      # DOCTYPE TAG
            ('<?', 'instruction'),  # INSTRUCTION TAG
            ('</', 'closing'),      # CLOSING TAG
            ('<', 'opening'),       # OPEN TAG
            (None, 'text'),         # TEXT TAG
        ])

        for prefix, kind in rules.items():
            if prefix:
                if like(stream, prefix):
                    yield tag(stream, kind)
                    break
            else:
                if not peek(stream) == '':
                    yield text(stream, 'text')


def text(stream, kind):
    acc = ''
    tec = stream.read(1)
    while tec != '<' and tec != '':
        acc += tec
        tec = stream.read(1)

    if peek(stream) != '':
        stream.seek(stream.tell() - 1)  # must rewind before '<'
        # only if not at the end.
    return kind, acc


def tag(stream, kind):
    acc = ''
    tac = stream.read(1)
    while tac != '>' and tac != '':
        acc += tac
        tac = stream.read(1)

    if tac == '':                        # PREMATURE EOF
        return 'error', acc
    else:
        # hold on, self closing ?
        if acc[-1] == '/':
            return 'selfclosing', acc + '>'            # SELFCLOSING
        else:
            return kind, acc + '>'
