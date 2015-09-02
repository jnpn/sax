'''
Classic imperative attempt
'''

def dummy(f):
    c = f.read()
    while c != '':
        yield c
        c = f.read()

def sax_root(stream):
    c = stream.read()
    while c != -1:
        if c == '<':
            k = stream.read()
            if k == '?':
                return sax_inst(stream)
            elif k == '/':
                return sax_ctag(stream)
            else:
                return sax_otag(stream)

def sax_inst(stream):
    """
    Docstrings are
    weird.
    """
    c = stream.read(1)
    inst = c
    while c != '?':
        inst += c
        c = stream.read(1)
    q = stream.read(1)
    b = stream.read(1)
    return inst + q + b

def sax_otag(stream): pass
def sax_ctag(stream): pass
def sax_text(stream): pass
