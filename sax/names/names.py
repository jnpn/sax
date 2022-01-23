'''
name module used for [namespaced] tag names
'''

import re

class Option:
    pass

class Name:
    nss = {}

    def __init__(self, n, ns=None):
        self.n = n
        self.ns = ns
        self.__ns_register()

    def __ns_register(self):
        if self.ns:
            e = Name.nss.get(self.ns, None)
            if e:
                e[self.n] = self
            else:
                Name.nss[self.ns] = {self.n: self}

    def closeable_by(self, other):
        return self == other

    def __eq__(self, other):
        print('=', self, other)
        return self.ns == other.ns and self.n == self.n

    def __repr__(self):
        return f'<Name {self.ns}:.{self.n}>' if self.ns else f'<Name {self.n}>'

def preload():
    ''' just some names to init Name.nss '''
    return [Name(tag,'xhtml') for tag in 'div pre p a main nav button form input ul li ol section footer h1 h2 h3 h4 h5 h6 span video head title body html'.split(' ')]

RX = re.compile('</?(?P<tag>[^\s>]+) ?(?P<attrs>.*)>', re.DOTALL)

def name(n, sep=':') -> Name:
    ''' constructor: str -> Name'''
    if sep in n:
        ns,name,*_ = n.split(':')
        if _:
            error = f'{name} is malformed. shoulde be [<ns>:]<name>'
            raise Exception(error,n)
        else:
            return Name(name, ns)
    else:
        return Name(n)

def parse(tagspec): # -> Option[(Name, list[Name])]:
    '''
    >>> parse('<div a=b>')
    (<Name div>, [(<Name a>, 'b')])
    >>> parse('<div a=b c d:e=f>')
    (<Name div>, [(<Name a>, 'b'), <Name c>, (<Name d:.e>, 'f')])
    >>> parse('<html:div a=b c d:e=f>')
    (<Name html:.div>, [(<Name a>, 'b'), <Name c>, (<Name d:.e>, 'f')])
    '''
    m = re.match(RX, tagspec)
    if m:
        g = m.groupdict()
        if g:
            tag = g['tag']
            tag = name(tag) if tag else tag
            attrs = g['attrs']
            attrs = parsekv(attrs)
            return (tag, attrs)
    return None

def parsekv(pairs, seppair=' ', sepkv="="): #-> list[(Name, Option[str])]:
    ''' [ns:?name(=val)?] -> [(Name(...), val?) ]
    >>> parsekv('a=b b=c d e f=g u:v=s:t')
    [(<Name a>, 'b'), (<Name b>, 'c'), <Name d>, <Name e>, (<Name f>, 'g'), (<Name u:.v>, 's:t')]
    '''
    def unkv(kv):
        '''
        k pairs...
        k=v pairs...
        '''
        xs = kv.split(sepkv)
        if len(xs) == 2: # k=v
            k,v = xs
            return name(k),v.replace('"','')
        if len(xs) == 1: # k
            k = xs[0]
            return name(k)
        # shouldn't ever happen
        raise Exception(f'{kv} malformed. Should be <k>=<v> or <k>')

    pairs = re.split(seppair+'+', pairs) 
    return [unkv(p) for p in pairs]
