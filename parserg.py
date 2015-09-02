from collections import namedtuple

Root = namedtuple('Root', 'children')
Inst = namedtuple('Inst', 'inst')
Text = namedtuple('Text', 'text')
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
        elif k == 'etag':
            sub = stack.pop();
            stack[-1].children.append(sub)
    print(stack)
    return stack[0]

def pp(xml):
    k = xml.__class__.__name__
    if k == 'Root':
        print('Root')
        for c in xml.children:
            pp(c)
    elif k == 'Text':
        print('Text', xml.text)
    elif k == 'Tag':
        print(xml.name)
        for c in xml.children:
            pp(c)
    elif k == 'Inst':
        print('Inst', xml.inst)
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

def test_xml():
    return xml(root(open('./samples/dbus.xml', 'rb')))


def test_0():
    t = xml(root(io.BytesIO(b'<foo>x</foo>')))
    return t

def test_1():
    '''bug'''
    t = xml(root(io.BytesIO(b'<foo><bar>duh</bar></foo>')))
    return t
