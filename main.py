'''

sax.py -- pure python xml parser

'''

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
    print({
        'author': 'jnpn',
        'version': '0.01a',
        'license': 'GPLv3'
    })

@click.group()
def cli():
    pass

cli.add_command(samples)
cli.add_command(tree)
cli.add_command(demo_tokenizer)
cli.add_command(demo_parser)
cli.add_command(about)

if __name__ == '__main__':
    cli()

