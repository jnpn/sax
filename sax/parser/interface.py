import re

from collections import namedtuple

from sax.names.names import name, Name

Root = namedtuple('Root', 'children')
Instruction = namedtuple('Instruction', 'instruction')
Text = namedtuple('Text', 'text')
Comment = namedtuple('Comment', 'comment')
Doctype = namedtuple('Doctype', 'doctype')
# Tag = namedtuple('Tag', 'name attrs children')

class Tag:

    def __init__(self, spec):
        self.spec = spec
        self.tag_regex = '</?\s*(?P<tagname>[a-zA-Z0-9:_\-]+)(\s+(?P<attrs>.*))?>'
        ### thanks https://regexr.com/6e6rh
        self.attr_kv_regex = '(?P<key>[a-zA-Z0-9:\-]+)(="(?P<val>[^"]+)")?'
        self._off_()
        self._on_()

    def _is_on_(self):
        return self.populated

    def _off_(self):
        self.populated = False
        self.name = ""
        self.attrs = []
        self.children = []
        # print('[reset]', self)

    def _on_(self):
        m = re.match(self.tag_regex, self.spec, re.MULTILINE + re.DOTALL)
        if m:
            g = m.groupdict()
            self.name = name(g['tagname'])
            a = g['attrs'] or ''
            self.attrs = [name(k,v) for k,_,v in re.findall(self.attr_kv_regex, a)]
            self.populated = True
        # print('[populated]', self)
    def is_closeable_by(self, closing):
        otn = self.name
        ctn = name(closing[2:-1])
        assert otn == ctn, "Wrong open/close tags: '%s' | '%s'" % (otn, ctn)
        if otn != ctn:
            raise MalformedXML(opentag, closetag)

    def __repr__(self):
        if self._is_on_():
            return f'<{self.__class__.__name__} {self.name} {self.attrs} {self.children}>'
        else:
            return f'<{self.__class__.__name__} {self.spec} unset>'

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
