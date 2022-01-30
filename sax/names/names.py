'''
module for namespaced names
'''

import re

class Name:
    requests = 0
    count = 0
    nss = {}

    def __init__(self, n, ns=None):
        self.n = n
        self.ns = ns
        self.__ns_register()

    def __in__(n,ns=None):
        ''' (ns,n) -> Maybe Name '''
        Name.requests += 1
        r = False
        # n
        if not ns:
            r = Name.nss.get(n, False)# Maybe Name
        # ns:n
        else:
            nso = Name.nss.get(ns, False) # {}
            if nso:
                r = nso.get(n, False)  # Maybe Name
        if r:
            # print('reused', n, ns, r)
            return r

    def __ns_register(self):
        if self.ns:
            e = Name.nss.get(self.ns, None)
            if e:
                e[self.n] = self
            else:
                Name.nss[self.ns] = {self.n: self}
            Name.count += 1

    def __eq__(self, other):
        if isinstance(other, str):
            other = name(other)
        # print('=', self, other)
        return self.ns == other.ns and self.n == other.n

    def __str__(self, sep=':'):
        return self.ns + sep + self.n if self.ns else self.n

    def __repr__(self):
        return f'<Name {self.ns}:.{self.n}>' if self.ns else f'<Name {self.n}>'

def preload():
    ''' just some names to init Name.nss '''
    tags = 'div pre p a main nav button form input ul li ol section footer h1 h2 h3 h4 h5 h6 span video head title body html'
    return [Name(tag,'xhtml') for tag in tags.split(' ')]

def name(n, sep=':') -> Name:
    ''' constructor: str -> Name'''
    if sep in n:
        ns,name,*_ = n.split(':')
        if _:
            error = f'{name} is malformed. shoulde be [<ns>:]<name>'
            raise Exception(error,n)
        else:
            return Name.__in__(name,ns) or Name(name, ns)
    else:
        return Name.__in__(n) or Name(n)
