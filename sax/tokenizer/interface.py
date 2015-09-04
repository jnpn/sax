'''
Objects defining the sax tokenizer interface.

Only used as unique symbols shared by implementations.
'''


class token:
    def __repr__(self, ):
        return 'token:%s' % self.__class__.__name__

class comment(token): pass
class doctype(token): pass
class opening(token): pass
class closing(token): pass
class selfclosing(token): pass
class instruction(token): pass
class text(token): pass
class error(token): pass

comment = comment()
doctype = doctype()
opening = opening()
closing = closing()
selfclosing = selfclosing()
instruction = instruction()
text = text()
error = error()

def peek(stream, forward):
    raise NotImplementedError("Interface stub only")


def tok(stream):
    raise NotImplementedError("Interface stub only")
