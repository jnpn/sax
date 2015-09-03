from nose.tools import assert_equal
import io
from sax.saxg import tok, peek

# peek

def test_peek():
    bnil = ''
    bsnil = io.StringIO(bnil)
    assert_equal(bnil, peek(bsnil))

# parsers

def test_text():
    bs = 'yolo'
    t = list(tok(io.StringIO(bs)))
    e = [('text', 'yolo')]
    # return bs, t, e, t == e
    assert_equal(t, e)


def test_text_opening():
    bs = 'text<foo>'
    t = list(tok(io.StringIO(bs)))
    e = [('test', 'text'),
         ('opening', '<foo>')]


def test_opening():
    bs = '<foo>'
    i = list(tok(io.StringIO(bs)))
    e = [('opening', '<foo>')]
    # return bs, i, e, i == e
    assert_equal(i, e)


def test_opening_closing():
    bs = '<foo></foo>'
    i = list(tok(io.StringIO(bs)))
    e = [('opening', '<foo>'),
         ('closing', '</foo>')]
    # return bs, i, e, i == e
    assert_equal(i, e)


def test_opening_opening():
    bs = '<foo><bar>'
    i = list(tok(io.StringIO(bs)))
    e = [('opening', '<foo>'),
         ('opening', '<bar>')]
    # return bs, i, e, i == e
    assert_equal(i, e)


def test_opening_attrs():
    bs = '<foo a="a" b="b">'
    i = list(tok(io.StringIO(bs)))
    e = [('opening', '<foo a="a" b="b">')]
    # return bs, i, e, i == e
    assert_equal(i, e)


def test_closing():
    bs = '</foo>'
    i = list(tok(io.StringIO(bs)))
    e = [('closing', '</foo>')]
    # return bs, i, e, i == e
    assert_equal(i, e)


def test_instruction_too_short():
    bs = '<?xml version="1.0" encoding="UTF-8"?'
    i = list(tok(io.StringIO(bs)))
    e = [('error', '<?xml version="1.0" encoding="UTF-8"?')]
    # return bs, i, e, i == e
    assert_equal(i, e)


def test_instruction():
    bs = '<?xml version="1.0" encoding="UTF-8"?>'
    i = list(tok(io.StringIO(bs)))
    e = [('instruction', '<?xml version="1.0" encoding="UTF-8"?>')]
    # return bs, i, e, i == e
    assert_equal(i, e)


def test_instruction_2():
    bs = '<?xml version="1.0" encoding="UTF-8"?><?instruction?>'
    i = list(tok(io.StringIO(bs)))
    e = [('instruction', '<?xml version="1.0" encoding="UTF-8"?>'),
         ('instruction', '<?instruction?>')]
    # return bs, i, e, i == e
    assert_equal(i, e)


def test_instruction_text():
    bs = '<?xml version="1.0" encoding="UTF-8"?>text'
    i = list(tok(io.StringIO(bs)))
    e = [('instruction', '<?xml version="1.0" encoding="UTF-8"?>'),
         ('text', 'text')]
    # return bs, i, e, i == e
    assert_equal(i, e)


def test_text_opening_text_closing():
    bs = 'eww<foo>bar</foo>'
    i = list(tok(io.StringIO(bs)))
    e = [('text', 'eww'),
         ('opening', '<foo>'),
         ('text', 'bar'),
         ('closing', '</foo>')]


def test_opening_text_closing():
    bs = '<foo>bar</foo>'
    i = list(tok(io.StringIO(bs)))
    e = [('opening', '<foo>'),
         ('text', 'bar'),
         ('closing', '</foo>')]

def test_instruction_text_instruction():
    bs = '<?xml version="1.0" encoding="UTF-8"?>text<?instruction?>'
    i = list(tok(io.StringIO(bs)))
    e = [('instruction', '<?xml version="1.0" encoding="UTF-8"?>'),
         ('text', 'text'),
         ('instruction', '<?instruction?>')]
    # return bs, i, e, i == e
    assert_equal(i, e)
