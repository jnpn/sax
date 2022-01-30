class Trie:
    '''
    trie 'k 'a {
        'k -> ['a]
      | 'k -> trie 'k 'a
    }
    '''

    def sub(self): # {}
        pass

    def leaves(self):
        pass

    def has(self, k): # bool
        return k in self.sub()

    def put(self, ks, v):
        # put trie ks v
        '''
        has(k) ks... -> recurse | self[k].put(ks,v)
        no k   ks... -> recurse | sub = self[k] = node(k); sub.put(ks, v)
        has(k) k     -> base  | insert-into leaf(k,v)
        no k   k     -> base  | insert-new Node leaf(k,v)
        '''
        if ks == None and v:
            self.leaves().append(v)
        elif len(ks) > 1: # RECURSE
            k,*ks = ks
            # if self.has(k):
            #     return self.sub().get(k).put(ks,v)
            if not self.has(k): # ENSURE self.sub().get(k) is Trie
                s = Node(k)
                self.sub()[k] = s
            self.sub().get(k).put(ks,v)
        else:
            k = ks[0]
            # if self.has(k):
            #     self.sub().get(k).leaves().append(v)
            # else:
            #     assert len(ks) == 1
            if not self.has(k):
                s = Node(k)
                self.sub()[k] = s
            self.sub().get(k).leaves().append(v)
        return self

    def get(self, ks):
        if len(ks) > 0:
            k,*ks = ks
            if self.has(k):
                return self.sub().get(k).get(ks)
            else:
                raise Exception(k, 'not found')
        return self.leaves()

    def Put(self, v, *ks):
        return self.put(ks, v)

    def Get(self, *ks):
        return self.get(ks)
            
    def __repr__(self):
        return f'<trie>'

class Root(Trie):
    def __init__(self):
        self.s = {}
        self.l = []

    def sub(self):
        return self.s

    def leaves(self):
        return self.l

    def __repr__(self):
        if self.sub():
            return f'(Trie  {self.sub()}{self.leaves()})'
        else:
            return f'(Trie. {self.leaves()})'

class Node(Root):
    def __init__(self, k):
        super().__init__()
        self.k = k
        

def t0():

    r = Root()
    for p,v in [
            (None, 'x'),
            ([0], 'b'),
            ([0,1], 'a'),
            ([0,1], 'b'),
            ([1,2], 'a'),
    ]:
        r.put(p,v)
    return r

def t1():
    r = Root()
    for ns,n in [
            (['xhtml'], 'div'),
            (['xhtml'], 'pre'),
            (['xhtml'], 'span'),
            (['xhtml'], 'p'),
            (['xhtml'], 'h1'),
            (['xml','ns'], 'element'),
            (['xml','ns'], 'attribute'),
            (['xml','ns','meta'], 'comment'),
    ]:
        r.put(ns,n)
    return r
