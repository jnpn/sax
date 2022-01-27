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


import re

tag_regex = '<(?P<tagname>[a-zA-Z0-9:_\-]+)( +(?P<attrs>.*))>'
attr_kv_regex = '(?P<key>[a-zA-Z0-9:\-]+)(="(?P<val>[a-zA-Z0-9:\-]+)")?' ### thanks https://regexr.com/6e6rh

class KV:
    def __init__(self, pair):
        k,_,v = pair
        self.k = k
        self.v = v if v else False

    def __repr__(self):
        if self.v:
            return f'{self.k}="{self.v}"'
        else:
            return f'{self.k}={self.v}'

def attrs(s):
    '''
    >>> attrs('a="b" c="d" e="f"')
    [a="b", c="d", e="f"]
    >>> attrs('a="b" c e="f"')
    [a="b", c=False, e="f"]
    '''
    return [KV(p) for p in re.findall(attr_kv_regex, s)]


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
        m = re.match(tag_regex, acc)
        if m:
            g = m.groupdict()
            tagname = g['tagname']
            s_attrs = g.get('attrs', None)
            if s_attrs:
                print(tagname, attrs(s_attrs))
            
    return k, acc
