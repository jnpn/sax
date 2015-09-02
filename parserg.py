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
            stack[-1].children.append(Tag(t, [], []))
        elif k == 'text':
            stack[-1].children.append(Text(t))
        elif k == 'etag':
            t = stack[-1];
            stack[-1].children.append(t)
    print(stack)
    return stack[0]

def test_xml():
    return xml(root(open('./samples/dbus.xml', 'rb')))
