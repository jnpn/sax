#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''sax.py -- pure python xml parser

Builds an in-memory tree of the xml file. With namespaced tag and attribute names.

End.
'''

__author__ = "Johan Ponin"
__copyright__ = "Copyright 2019-, jnpn"
__credits__ = ["Johan Ponin"]
__license__ = "GPLv3"
__version__ = "0.0.1a2"
__maintainer__ = "Johan Ponin"
__email__ = "johan.ponin.pro@gmail.com"
__status__ = "Alpha"

import os
import pprint

import click

import sax.tokenizer.gen as gt
import sax.tokenizer.loop as lt

import sax.names.names as ns

SAMPLES = './samples'

@click.command()
@click.argument('xmlfile', type=click.File('r'))
def tree(xmlfile):
    """Parses XML file and prints a `tree` representation of it."""
    from sax.parser.core import pp, xml
    print(pp(xml(lt.tok(xmlfile))))

@click.command()
def demo_tokenizer(fn=SAMPLES + '/cv.meta.xml'):
    ''' Shows tokenizer output '''
    for k,t in lt.tok(open(fn)):
        print(k,t, type(t))

@click.command()
def demo_parser(fn=SAMPLES+'/lclo_m.xml'):
    ''' Shows parser output (with namespace) '''
    print(f'parsing {fn}')
    from sax.parser.core import pp, xml
    tree = xml(lt.tok(open(fn)))
    pp(tree)
    print('xmlns', pprint.pformat(ns.Name.nss))
    return tree


@click.command()
def samples():
    """Lists the XML provided samples."""
    for sample in os.listdir(SAMPLES):
        print(os.path.sep.join([SAMPLES, sample]))

@click.command()
def about():
    """Shows information about this."""
    print()
    print(__doc__)
    for info in ['__author__', '__copyright__',
                 '__credits__', '__email__', '__license__',
                 '__maintainer__', '__status__', '__version__',
                 '__file__']:
        print(info.replace('_',''), ':', eval(info))
    print({
        'author': 'jnpn',
        'version': '0.01a',
        'license': 'GPLv3'
    })
    print()

@click.group()
@click.version_option(__version__)
@click.pass_context
def cli(ctx):
    pass

cli.add_command(samples)
cli.add_command(tree)
cli.add_command(demo_tokenizer)
cli.add_command(demo_parser)
cli.add_command(about)

from sax.parser.core import pp, xml
from sax.names.names import Name
def bch(fn=SAMPLES+'/cv.xml'):
    return xml(lt.tok(open(fn))), Name


import timeit

'''
timeit.timeit(bch, number=3)
>>> 0.22704315300052258 # str
>>> 0.22025592699992558 # StringIO
timeit.timeit(bch, number=30)
>>> 2.130348282000341
>>> 2.126030572999298
timeit.timeit(bch, number=100)
>>> 7.017249186000299
>>> 7.329132808000395
'''

if __name__ == '__main__':
    cli()
