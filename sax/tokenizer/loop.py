'''
Classic imperative attempt
'''

from sax.tokenizer.exceptions import UnknownElement
from sax.prelude import peek
from sax.tokenizer.interface import comment, doctype, opening, \
    closing, selfclosing, instruction, text, error


lc = 1  # line count
lo = 0  # line offset


def tok(stream):
    global lo
    global lc

    while peek(stream) != '':

        c = peek(stream)
        k = None
        pre_lc = lc
        pre_lo = lo

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
            _update_(tac)

            while tac != '>' and tac != '':
                acc += tac
                tac = stream.read(1)
                _update_(tac)
            pse = stream.tell()

            if tac == '':                        # PREMATURE EOF
                k = error
                yield k, acc, (psb, pse, pre_lc, pre_lo)
            else:
                # hold on, self closing ?
                if acc[-1] == '/':
                    k = selfclosing              # SELFCLOSING

                acc += '>'
                yield k, acc, (psb, pse, pre_lc, pre_lo)

        else:                                    # TEXT
            k = text
            psb = stream.tell()
            acc = ''
            tec = stream.read(1)
            _update_(tec)
            while tec != '<' and tec != '':
                acc += tec
                tec = stream.read(1)
                _update_(tec)

            if peek(stream) != '':
                stream.seek(stream.tell() - 1)  # must rewind before '<'
                # only if not at the end.
                lo -= 1  # lo is impacted. Maybe lc too ? T_T

            pse = stream.tell()
            yield k, acc, (psb, pse, pre_lc, pre_lo)


def _update_(c):
    global lc, lo
    if c == '\n':
        lc += 1
        lo = 0
    else:
        lo += 1
