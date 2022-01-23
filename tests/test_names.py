'''test
from sax.parser.core import pp, xml
pp(xml(lt.tok(open('./samples/cv.meta.xml'))))

from sax.parser.core import pp, xml
pp(xml(lt.tok(open('./samples/lclo.xml'))))

from sax.parser.core import pp, xml
pp(xml(lt.tok(open('./samples/cv.settings.xml'))))

pp(xml(lt.tok(open('./samples/cv.xml'))))
'''

def preload():
    ''' just some names to init Name.nss '''
    return [Name(tag,'xhtml') for tag in 'div pre p a main nav button form input ul li ol section footer h1 h2 h3 h4 h5 h6 span video head title body html'.split(' ')]

