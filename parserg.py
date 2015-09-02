from collections import namedtuple
import io

from saxg import root


Root = namedtuple('Root', 'children')
Inst = namedtuple('Inst', 'inst')
Text = namedtuple('Text', 'text')
Comment = namedtuple('Comment', 'comment')
Doctype = namedtuple('Doctype', 'doctype')
Tag = namedtuple('Tag', 'name attrs children')
# Tag('foo', [], [Text('wat'), Text('duh')])

def xml(token_stream):
    stack = []

    stack.append(Root([]))
    for k, t in token_stream:
        if k == 'inst':
            top(stack).children.append(Inst(t))
        elif k == 'otag':
            stack.append(Tag(t, [], []))           # SHIFT
        elif k == 'text':
            top(stack).children.append(Text(t))    # SELF INSERT
        elif k == 'comment':
            top(stack).children.append(Comment(t)) # SELF INSERT
        elif k == 'doctype':
            top(stack).children.append(Doctype(t)) # SELF INSERT
        elif k == 'etag':
            sub = stack.pop()                      # REDUCE
            top(stack).children.append(sub)
    return fst(stack)


def pp(xml):
    k = xml.__class__.__name__
    if k == 'Root':
        print('Root')
        for c in xml.children:
            pp(c)
    elif k == 'Text':
        print('Text', xml.text.decode('utf8').strip())
    elif k == 'Comment':
        print('comment', xml.comment.decode('utf8').strip())
    elif k == 'Doctype':
        print('Doctype', xml.doctype.decode('utf8').strip())
    elif k == 'Tag':
        print(xml.name)
        for c in xml.children:
            pp(c)
    elif k == 'Inst':
        print('Inst', k, xml.inst.decode('utf8').strip())
    else:
        print('[unknown]', xml)

'''
pp(Root([Tag('foo',[],[Inst('doctype'), Text('wat'), Tag('bar', [], [Text('duh')])])]))
->
Root
foo
Inst doctype
Text wat
bar
Text duh
# OK
'''


def fst(s):
    return s[0]


def top(s):
    return s[-1]
