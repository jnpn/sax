'''
Classic imperative attempt
'''

from sax.tokenizer.exceptions import UnknownElement
from sax.prelude import peek
from sax.tokenizer.interface import comment, doctype, opening, \
    closing, selfclosing, instruction, text, error


def tok(stream):

    while peek(stream) != '':
        c = peek(stream)
        if c == '<':                             # * TAG
            acc = ''
            tac = stream.read(1)
            while tac != '>' and tac != '':
                acc += tac
                tac = stream.read(1)
            if tac == '':                        # PREMATURE EOF
                k = error
                yield k, acc
            else:
                acc += '>'                       # Inclusive parsing terminal

                yield tag(acc)

        else:                                    # TEXT
            k = text
            acc = ''
            tec = stream.read(1)
            while tec != '<' and tec != '':
                acc += tec
                tec = stream.read(1)

            if peek(stream) != '':
                stream.seek(stream.tell() - 1)  # must rewind before '<'
                # only if not at the end.
            yield k, acc


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
