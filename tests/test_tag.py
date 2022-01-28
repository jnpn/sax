import io

from nose.tools import assert_equal, raises, assert_not_equal

from sax.parser.exceptions import MalformedXML
import sax.parser.interface as c


def test_tag_name():
    u = c.Tag('<foo>')
    assert_equal(u.name.n, 'foo')

def test_tag_name():
    u = c.Tag('<ml:foo>')
    assert_equal(u.name.ns, 'ml')

def test_is_closeable_by():
    u = c.Tag('<foo>')
    v = c.Tag('</foo>')
    assert_equal(u.is_closeable_by(v), True)

@raises(MalformedXML)
def test_is_closeable_by_not():
    u = c.Tag('<foo>')
    w = c.Tag('</bar>')
    return u.is_closeable_by(w)

