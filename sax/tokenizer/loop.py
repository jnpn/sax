'''
Classic imperative attempt
'''

import io

from sax.tokenizer.exceptions import UnknownElement
from sax.prelude import peek
from sax.tokenizer.interface import comment, doctype, opening, \
    closing, selfclosing, instruction, text, error


def tok(stream):

    acc = io.StringIO()

    while peek(stream) != '':
        c = peek(stream)
        if c == '<':                             # * TAG
            acc.truncate(0)
            acc.seek(0)
            tac = stream.read(1)
            while tac != '>' and tac != '':
                acc.write(tac)
                tac = stream.read(1)
            if tac == '':                        # PREMATURE EOF
                k = error
                yield k, acc.getvalue()
            else:
                acc.write('>')                   # Inclusive parsing terminal

                yield tag(acc.getvalue())

        else:                                    # TEXT
            k = text
            acc.truncate(0)
            acc.seek(0)
            tec = stream.read(1)
            while tec != '<' and tec != '':
                acc.write(tec)
                tec = stream.read(1)

            if peek(stream) != '':
                stream.seek(stream.tell() - 1)  # must rewind before '<'
                # only if not at the end.
            yield k, acc.getvalue()


def tag(acc):
    '''
    instruction '<? ... ?>'
    comment '<!-- ... -->'
    doctype '<!doctype ...>' | '<!DOCTYPE ...>'
    selfclosing '<.../>'
    closing '</...>'
    tag '<*>'
    '''
    if acc.startswith('<?') and acc.endswith('?>'):
        k = instruction
    elif acc.startswith('<?') and not acc.endswith('?>'):
        k = error
    elif acc.startswith('<!--') and acc.endswith('-->'):
        k = comment
    elif acc.startswith('<!--') and not acc.endswith('-->'):
        k = error
    elif acc.startswith('<!doctype') or acc.startswith('<!DOCTYPE'):
        k = doctype
    elif acc.endswith('/>') and not acc.startswith('</'):
        k = selfclosing
    elif acc.startswith('</'):
        k = closing
    else:
        k = opening
    return k, acc
