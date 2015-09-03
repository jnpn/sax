from nose.tools import assert_equal

import io

from saxi import peek, tok


def testpeek0():
    c = peek(io.StringIO('<foo>'), off=2)
    e = 'f'
    assert_equal(c, e)


def testpeek1():
    c = peek(io.StringIO('<foo>'), off=3)
    e = 'o'
    assert_equal(c, e)


def test_tok_text():
    import io
    e = [('text', 'foo')]
    t = list(tok(io.StringIO('foo')))
    assert_equal(t, e)


def test_tok_tag():
    import io
    e = [('opening', '<foo>')]
    t = list(tok(io.StringIO('<foo>')))
    assert_equal(t, e)


def test_tok_inst():
    import io
    e = [('instruction', '<?foo?>')]
    t = list(tok(io.StringIO('<?foo?>')))
    assert_equal(t, e)


def test_tok_selfclosing():
    import io
    e = [('selfclosing', '<foo/>')]
    t = list(tok(io.StringIO('<foo/>')))
    assert_equal(t, e)
