from collections import namedtuple

Root = namedtuple('Root', 'children')
Instruction = namedtuple('Instruction', 'instruction')
Text = namedtuple('Text', 'text')
Comment = namedtuple('Comment', 'comment')
Doctype = namedtuple('Doctype', 'doctype')
Tag = namedtuple('Tag', 'name attrs children')


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
