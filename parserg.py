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
            stack[-1].children.append(Inst(t))
        elif k == 'otag':
            stack.append(Tag(t, [], []))
        elif k == 'text':
            stack[-1].children.append(Text(t))
        elif k == 'comment':
            stack[-1].children.append(Comment(t))
        elif k == 'doctype':
            stack[-1].children.append(Doctype(t))
        elif k == 'etag':
            sub = stack.pop();
            stack[-1].children.append(sub)
    return stack[0]


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



def strcopy(buf):
    s = buf.read()
    buf.seek(0)
    return s


# tests

def test_xml():
    s = open('./samples/dbus.xml', 'rb')
    print(strcopy(s))
    return xml(root(s))


def test_0():
    s = io.BytesIO(b'<foo>x</foo>')
    print(strcopy(s))
    t = xml(root(s))
    return t

def test_1():
    '''bug'''
    s = io.BytesIO(b'<foo><bar>duh</bar></foo>')
    print(strcopy(s))
    t = xml(root(s))
    return t
