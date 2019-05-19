from sax.tokenizer.interface import *
from sax.tokenizer import loop

from sax.parser.core import tagname

class NestingException(Exception):
    pass

class Unsax:
    def opening(self, kind, acc):
        pass
    def closing(self, kind, acc):
        pass
    def ignored(self, kind, acc):
        pass


class Dummy(Unsax):
    def __init__(self):
        self.depth = 0
        print('[init]', '_%d' % self.depth)
    def opening(self, kind, acc):
        self.depth += 1
        print('[opening]', '%d>' % self.depth, kind, acc)
    def closing(self, kind, acc):
        self.depth -= 1
        print('[closing]', '<%d' % self.depth, kind, acc)
    def ignored(self, kind, acc):
        print('[ignored]', '%d_' % self.depth, kind, acc)


def check(tokens, unsax=Dummy()):
    '''ensure proper nesting of tags'''
    stack = []
    for kind, _ in tokens:
        if kind is opening:
            stack += [tagname(_)]
            unsax.opening(kind, _)
        if kind is closing:
            if stack[-1] == tagname(_):
                stack.pop()
                unsax.closing(kind, _)
            else:
                raise NestingException(kind, _, stack)

        # below are ignored tokens
        if kind is comment:
            pass
        if kind is doctype:
            pass
        if kind is selfclosing:
            pass
        if kind is instruction:
            pass
        if kind is text:
            pass
        if kind is error:
            pass

    assert len(stack) == 0, "Stack is not empty, probably unbalanced tree"

    return True
