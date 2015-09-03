from collections import namedtuple

from sax.tokenizer.interface import comment, doctype, opening, \
    closing, selfclosing, instruction, text

# Definitions

Root = namedtuple('Root', 'children')
Instruction = namedtuple('Instruction', 'instruction')
Text = namedtuple('Text', 'text')
Comment = namedtuple('Comment', 'comment')
Doctype = namedtuple('Doctype', 'doctype')
Tag = namedtuple('Tag', 'name attrs children')


class MalformedXML(Exception):
    pass


# Parser

def xml(token_stream):

    stack = [Root([])]

    for k, t in token_stream:
        if k == instruction:
            top(stack).children.append(Instruction(t))
        elif k == opening:
            stack.append(Tag(t, [], []))            # SHIFT
        elif k == text:
            top(stack).children.append(Text(t))     # SELF INSERT
        elif k == comment:
            top(stack).children.append(Comment(t))  # SELF INSERT
        elif k == doctype:
            top(stack).children.append(Doctype(t))  # SELF INSERT
        elif k == selfclosing:
            top(stack).children.append(Tag(t, [], []))  # SELF INSERT
        elif k == closing:
            sub = stack.pop()
            tagcheck(sub.name, t)                   # CHECK
            top(stack).children.append(sub)         # REDUCE
    return fst(stack)


def tagcheck(opentag, closetag):
    otn = tagname(opentag)
    ctn = tagname(closetag)
    assert otn == ctn, "Wrong open/close tags: <%s> | </%s>" % (otn, ctn)
    if otn != ctn:
        raise MalformedXML(opentag, closetag)


def tagname(tag):
    import re
    rx = '</?(?P<tag>[^ >]+).*>'
    return re.match(rx, tag).groupdict()['tag']


def fst(s):
    return s[0]


def top(s):
    return s[-1]


# Pretty Printer

def pp(xml, inds=0, indc='  '):

    def clean(s):
        import re
        s = s.strip()
        return re.sub(r'[\t\r\n ]+', ' ', s)

    def pic(k, t, post=lambda k, v: k + ' ' + v):
        '''Print Indented and Clean'''
        print(indc * inds, post(k, clean(t)))

    def pre(c):
        return lambda s: c + s

    k = xml.__class__.__name__
    if k == 'Root':
        print(indc * inds, 'Root')
        for c in xml.children:
            pp(c, inds + 1)
    elif k == 'Text':
        pic(k, xml.text)
    elif k == 'Comment':
        pic(k, xml.comment)
    elif k == 'Doctype':
        pic(k, xml.doctype)
    elif k == 'Tag':
        pic(k, xml.name)
        for c in xml.children:
            pp(c, inds + 1)
        pic(k, xml.name, post=lambda k, v: ' /')
    elif k == 'Instruction':
        pic(k, xml.instruction)
    else:
        pic('[unknown]', xml)


def xmldepth(xml):

    def isnode(n):
        return n == 'Root' or n == 'Tag'

    def isleaf(n):
        return n == 'Instruction' or n == 'Text' or n == 'Doctype' or n == 'Comment'

    k = xml.__class__.__name__

    if isnode(k):
        return 1 + max(map(xmldepth, xml.children), default=0)
    elif isleaf(k):
        return 1
