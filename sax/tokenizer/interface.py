'''
Objects defining the sax tokenizer interface.

Only used as unique symbols shared by implementations.
'''

class token: pass
class comment(token): pass
class doctype(token): pass
class opening(token): pass
class closing(token): pass
class selfclosing(token): pass
class instruction(token): pass
class text(token): pass

def peek(stream, forward): raise NotImplementedError
def tok(stream): raise NotImplementedError
