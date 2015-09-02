from collections import namedtuple

# Definitions

Root = namedtuple('Root', 'children')
Inst = namedtuple('Inst', 'inst')
Text = namedtuple('Text', 'text')
Comment = namedtuple('Comment', 'comment')
Doctype = namedtuple('Doctype', 'doctype')
Tag = namedtuple('Tag', 'name attrs children')


class MalformedXML(Exception):
    pass


# Parser

def xml(token_stream):
    stack = []

    stack.append(Root([]))
    for k, t in token_stream:
        if k == 'inst':
            top(stack).children.append(Inst(t))
        elif k == 'otag':
            stack.append(Tag(t, [], []))            # SHIFT
        elif k == 'text':
            top(stack).children.append(Text(t))     # SELF INSERT
        elif k == 'comment':
            top(stack).children.append(Comment(t))  # SELF INSERT
        elif k == 'doctype':
            top(stack).children.append(Doctype(t))  # SELF INSERT
        elif k == 'etag':
            sub = stack.pop()                       # REDUCE
            tns = tagname(sub.name)
            tnt = tagname(t)
            assert tns == tnt, "Wrong open/close tags: %s | %s" % (tns, tnt)
            if tns != tnt:
                raise MalformedXML(top(stack), sub)
            top(stack).children.append(sub)
    return fst(stack)


def tagname(tag):
    import re
    rx = b'</?(?P<tag>[^ >]+).*>'
    return re.match(rx, tag).groupdict()['tag']


def fst(s):
    return s[0]


def top(s):
    return s[-1]


# Pretty Printer

def pp(xml, inds=0, indc='  '):

    def clean(s):
        import re
        s = s.decode('utf8').strip()
        return re.sub(r'[\t\r\n ]+', ' ', s)

    k = xml.__class__.__name__
    if k == 'Root':
        print(indc * inds, 'Root')
        for c in xml.children:
            pp(c, inds + 1)
    elif k == 'Text':
        print(indc * inds, 'Text', clean(xml.text))
    elif k == 'Comment':
        print(indc * inds, 'comment', clean(xml.comment))
    elif k == 'Doctype':
        print(indc * inds, 'Doctype', clean(xml.doctype))
    elif k == 'Tag':
        print(indc * inds, clean(xml.name) + '[otag]')
        for c in xml.children:
            pp(c, inds + 1)
        print(indc * inds, clean(xml.name) + '[etag]')
    elif k == 'Inst':
        print(indc * inds, 'Inst', k, clean(xml.inst))
    else:
        print(indc * inds, '[unknown]', xml)
