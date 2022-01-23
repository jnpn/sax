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

    def __repr__(self):
        return f'{self.ns}:.{self.n}' if self.ns else self.n

def preload():
    ''' just some names to init Name.nss '''
    return [Name(tag,'xhtml') for tag in 'div pre p a main nav button form input ul li ol section footer h1 h2 h3 h4 h5 h6 span video head title body html'.split(' ')]
