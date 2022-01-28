import re

from collections import namedtuple

from sax.names.names import name, Name

Root = namedtuple('Root', 'children')
Instruction = namedtuple('Instruction', 'instruction')
Text = namedtuple('Text', 'text')
Comment = namedtuple('Comment', 'comment')
Doctype = namedtuple('Doctype', 'doctype')

class Tag:

    def __init__(self, spec:str, children=[]):
        self.tag_r    = '</?\s*(?P<tag>[a-zA-Z0-9:_\-]+)(\s+(?P<attrs>.*))?/? ?>'
        self.kv_r     = '(?P<key>[a-zA-Z0-9:\-]+)(="(?P<val>[^"]+)")?'     ### thanks https://regexr.com/6e6rh
        self.spec     = spec
        self.children = children[:]
        m = re.match(self.tag_r, self.spec, re.MULTILINE + re.DOTALL)
        if m:
            g = m.groupdict()
            self.name = name(g['tag'])
            a = g['attrs'] or ''
            self.attrs = [(name(k),v) for k,_,v in re.findall(self.kv_r, a)]
        else:
            raise Exception(spec, ' fails', self.tag_r, m)

    def is_closeable_by(self, closing):
        otn = self.name
        ctn = name(closing[2:-1])
        assert otn == ctn, "Wrong open/close tags: '%s' | '%s'" % (otn, ctn)
        if otn != ctn:
            raise MalformedXML(opentag, closetag)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name} {self.attrs} {self.children}>'

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
