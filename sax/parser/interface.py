import re

from collections import namedtuple

from sax.parser.exceptions import UnbalancedClosingTags, MalformedXML
from sax.names.names import name, Name

Root = namedtuple('Root', 'children')
Instruction = namedtuple('Instruction', 'instruction')
Text = namedtuple('Text', 'text')
Comment = namedtuple('Comment', 'comment')
Doctype = namedtuple('Doctype', 'doctype')

class Tag:
    '''
    Generic XML Node (tag, attrs, children...)
    '''

    def __init__(self, spec:str, children=[]):
        self.tag_r    = '</?\s*(?P<tag>[a-zA-Z0-9:_\-]+)(\s+(?P<attr>.*))?/? ?>'
        self.kv_r     = '(?P<key>[a-zA-Z0-9:\-]+)(="(?P<val>[^"]+)")?'
        ###                 ^-- thanks https://regexr.com/6e6rh
        self.spec     = spec
        self.children= children[:]
        m = re.match(self.tag_r, self.spec, re.MULTILINE + re.DOTALL)
        if m:
            g = m.groupdict()
            self.name = name(g['tag'])
            a = g['attr'] or ''
            self.attrs = [(name(k),v) for k,_,v in re.findall(self.kv_r, a)]
        else:
            raise MalformedXML(spec, ' fails', self.tag_r, m)

    def is_closeable_by(self, closing):
        ''' Tag -> Tag -> Boolean '''
        if self.name == closing.name:
            return True
        else:
            raise UnbalancedClosingTags(self, closing)

    def __eq__(self, other):
        return self.name == other.name \
            and self.attrs == other.attrs \
            and self.children == other.children

    def __repr__(self):
        cn = self.__class__.__name__
        return f'<{cn} {self.name} {self.attrs} {self.children}>'

def xml(stream):
    '''Stream -> XML'''
    raise NotImplementedError("Interface stub only")


def is_balanced(stream):
    '''XML balance predicate.'''
    '''
    is_balanced <foo></foo> -> True
    is_balanced <foo>       -> False
    is_balanced <foo></bar> -> False

    Fri Oct  9 17:33:55 CEST 2015: see: checker.py
    '''
    raise NotImplementedError("Interface stub only")
