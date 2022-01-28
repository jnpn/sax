'''test
from sax.parser.core import pp, xml
pp(xml(lt.tok(open('./samples/cv.meta.xml'))))

from sax.parser.core import pp, xml
pp(xml(lt.tok(open('./samples/lclo.xml'))))

from sax.parser.core import pp, xml
pp(xml(lt.tok(open('./samples/cv.settings.xml'))))
'''
from nose.tools import assert_equal, raises, assert_not_equal

from sax.names.names import name

def test_name_instanciates():
    n = name('xmlns:anchor')
    assert_equal(n, n)

def test_name_instanciates():
    n = name('xmlns:anchor')
    assert_equal(n, n)

def test_name_ns():
    n = name('xmlns:anchor')
    assert_equal(n.ns, 'xmlns')

def test_name_instanciates():
    n = name('xmlns:anchor')
    assert_equal(n.n, 'anchor')
    
