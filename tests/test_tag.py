import io

import pytest

from sax.parser.exceptions import UnbalancedClosingTags, MalformedXML
import sax.parser.interface as c


def test_tag_name():
    u = c.Tag('<foo>')
    assert u.name.n == 'foo'

def test_tag_name():
    u = c.Tag('<ml:foo>')
    assert u.name.ns == 'ml'

def test_is_closeable_by():
    u = c.Tag('<foo>')
    v = c.Tag('</foo>')
    assert u.is_closeable_by(v) == True

def test_is_closeable_by_not():
    u = c.Tag('<foo>')
    w = c.Tag('</bar>')
    with pytest.raises(UnbalancedClosingTags):
        return u.is_closeable_by(w)

