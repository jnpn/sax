from nose.tools import assert_equal
import io
from sax import root, peek

# peek

def test_peek():
    bnil = b''
    bsnil = io.BytesIO(bnil)
    assert_equal(bnil, peek(bsnil))

# parsers

def test_text():
    bs = b'yolo'
    t = list(root(io.BytesIO(bs)))
    e = [('text', b'yolo')]
    # return bs, t, e, t == e
    assert_equal(t, e)


def test_text_otag():
    bs = b'text<foo>'
    t = list(root(io.BytesIO(bs)))
    e = [('test', b'text'),
         ('otag', b'<foo>')]


def test_otag():
    bs = b'<foo>'
    i = list(root(io.BytesIO(bs)))
    e = [('otag', b'<foo>')]
    # return bs, i, e, i == e
    assert_equal(i, e)


def test_otag_etag():
    bs = b'<foo></foo>'
    i = list(root(io.BytesIO(bs)))
    e = [('otag', b'<foo>'),
         ('etag', b'</foo>')]
    # return bs, i, e, i == e
    assert_equal(i, e)


def test_otag_otag():
    bs = b'<foo><bar>'
    i = list(root(io.BytesIO(bs)))
    e = [('otag', b'<foo>'),
         ('otag', b'<bar>')]
    # return bs, i, e, i == e
    assert_equal(i, e)


def test_otag_attrs():
    bs = b'<foo a="a" b="b">'
    i = list(root(io.BytesIO(bs)))
    e = [('otag', b'<foo a="a" b="b">')]
    # return bs, i, e, i == e
    assert_equal(i, e)


def test_etag():
    bs = b'</foo>'
    i = list(root(io.BytesIO(bs)))
    e = [('etag', b'</foo>')]
    # return bs, i, e, i == e
    assert_equal(i, e)


def test_inst_too_short():
    bs = b'<?xml version="1.0" encoding="UTF-8"?'
    i = list(root(io.BytesIO(bs)))
    e = [('error', b'<?xml version="1.0" encoding="UTF-8"?')]
    # return bs, i, e, i == e
    assert_equal(i, e)


def test_inst():
    bs = b'<?xml version="1.0" encoding="UTF-8"?>'
    i = list(root(io.BytesIO(bs)))
    e = [('inst', b'<?xml version="1.0" encoding="UTF-8"?>')]
    # return bs, i, e, i == e
    assert_equal(i, e)


def test_inst_2():
    bs = b'<?xml version="1.0" encoding="UTF-8"?><?inst?>'
    i = list(root(io.BytesIO(bs)))
    e = [('inst', b'<?xml version="1.0" encoding="UTF-8"?>'),
         ('inst', b'<?inst?>')]
    # return bs, i, e, i == e
    assert_equal(i, e)


def test_inst_text():
    bs = b'<?xml version="1.0" encoding="UTF-8"?>text'
    i = list(root(io.BytesIO(bs)))
    e = [('inst', b'<?xml version="1.0" encoding="UTF-8"?>'),
         ('text', b'text')]
    # return bs, i, e, i == e
    assert_equal(i, e)


def test_text_otag_text_etag():
    bs = b'eww<foo>bar</foo>'
    i = list(root(io.BytesIO(bs)))
    e = [('text', b'eww'),
         ('otag', b'<foo>'),
         ('text', b'bar'),
         ('etag', b'</foo>')]


def test_otag_text_etag():
    bs = b'<foo>bar</foo>'
    i = list(root(io.BytesIO(bs)))
    e = [('otag', b'<foo>'),
         ('text', b'bar'),
         ('etag', b'</foo>')]

def test_inst_text_inst():
    bs = b'<?xml version="1.0" encoding="UTF-8"?>text<?inst?>'
    i = list(root(io.BytesIO(bs)))
    e = [('inst', b'<?xml version="1.0" encoding="UTF-8"?>'),
         ('text', b'text'),
         ('inst', b'<?inst?>')]
    # return bs, i, e, i == e
    assert_equal(i, e)
