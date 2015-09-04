'''
Classic imperative attempt
'''

from sax.tokenizer.exceptions import UnknownElement
from sax.prelude import peek
from sax.tokenizer.interface import comment, doctype, opening, \
    closing, selfclosing, instruction, text, error

lc = 0   # line count


def tok(stream):

    while peek(stream) != '':
        c = peek(stream)
        k = None

        # offside accounting
        if c == '\n':
            global lc
            lc += 1

        if c == '<':                             # * TAG
            cc = peek(stream, off=2)
            if cc == '?':
                k = instruction                  # INSTRUCTION TAG
            elif cc == '/':
                k = closing                      # CLOSING TAG
            elif cc == '!':
                ccc = peek(stream, off=3)
                if ccc == '-':
                    k = comment                  # COMMENT TAG
                elif ccc in {'d', 'D'}:
                    k = doctype                  # DOCTYPE TAG
                else:
                    raise UnknownElement(c + cc + ccc)
            else:
                k = opening                      # OPEN TAG

            # TAG work here
            psb = stream.tell()
            acc = ''
            tac = stream.read(1)
            while tac != '>' and tac != '':
                acc += tac
                tac = stream.read(1)
            pse = stream.tell()

            if tac == '':                        # PREMATURE EOF
                k = error
                yield k, acc, (psb, pse)
            else:
                # hold on, self closing ?
                if acc[-1] == '/':
                    k = selfclosing              # SELFCLOSING

                acc += '>'
                yield k, acc, (psb, pse)

        else:                                    # TEXT
            k = text
            psb = stream.tell()
            acc = ''
            tec = stream.read(1)
            while tec != '<' and tec != '':
                acc += tec
                tec = stream.read(1)

            if peek(stream) != '':
                stream.seek(stream.tell() - 1)  # must rewind before '<'
                # only if not at the end.
            pse = stream.tell()
            yield k, acc, (psb, pse)
