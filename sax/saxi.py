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


def eos(stream):
    return peek(stream) == ''


def tok(stream):

    while not eos(stream):
        print('[debug]', stream.tell(), eos(stream))
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
                if not eos(stream):
                    yield text(stream)
                    # stream.read(1)  # Eww T_T


# def text(stream, kind):
#     acc = ''
#     tec = stream.read(1)
#     while tec != '<' and tec != '':
#         acc += tec
#         tec = stream.read(1)

#     if peek(stream) != '':  # post-rewind
#         stream.seek(stream.tell() - 1)  # must rewind before '<'
#         # only if not at the end.
#     return kind, acc

# TODO abstract text and tag, see README.org  Imperative code : factorization


# def tag(stream, kind):
#     acc = ''
#     tac = stream.read(1)
#     while tac != '>' and tac != '':
#         acc += tac
#         tac = stream.read(1)

#     if tac == '':                        # PREMATURE EOF
#         return 'error', acc
#     else:
#         acc = acc + '>'  # post-append
#         # hold on, self closing ?
#         return ('selfclosing', acc) if acc[-1] == '/' else (kind, acc)


def take(pred, stream):
    acc = ''
    while not eos(stream):
        if pred(peek(stream)):
            acc += stream.read(1)
        else:
            break
    return eos(stream), acc


def parse_while(s, c, inclusive):
    prem, acc = take(lambda k: k != c, s)
    if prem:
        return prem, acc
    else:
        if inclusive:
            s.read(1)  # ugly but necessary drop
            return prem, acc + c
        else:
            return prem, acc


def tag(s, k):
    premature, a = parse_while(s, '>', True)
    if premature:
        return ('error', a)
    else:
        if a[-2] == '/':
            return ('selfclosing', a)
        else:
            return (k, a)


def rewind(s, n):
    p = s.tell()
    s.seek(p - n if p > n else p)


def text(s):
    premature, a = parse_while(s, '<', False)
    if premature:
        rewind(s, 1)
    else:
        return ('text', a)
