import os

import click

import sax.tokenizer.gen as gt
import sax.tokenizer.loop as lt

import sax.names.names as ns

SAMPLES = './samples'

src = './samples/dbus-systemd1.xml'

tsg = list(gt.tok(open(src)))
tsl = list(lt.tok(open(src)))


def k(n=32):
    for k, t in tsl[:n]:
        print(k, t)


diffs = [(g, l) for g, l in zip(tsg, tsl) if g != l]

'''
Intersting, parsers have different streams. Mostly out of
sync because of the selfclosing `tokenistic sugar` trick,
causing more tokens emitted by gen.tok:

<sctag/> -> (opening, sctag), (closing, sctag)

instead of

<sctag/> -> (selfclosing, sctag)

but may resolve the same trees when parsed.
'''

@click.command()
@click.argument('xmlfile', type=click.File('r'))
def tree(xmlfile):
    """Parses XML file and prints a `tree` representation of it."""
    from sax.parser.core import pp, xml
    print(pp(xml(lt.tok(xmlfile))))

def t(fn='./samples/cv.meta.xml'):
    for k,t in lt.tok(open(fn)):
        print(k,t, type(t))

# def u(fn='./samples/cv.meta.xml', show=True):
def u(fn='./samples/lclo_m.xml', show=True):
    print(f'parsing {fn}')
    from sax.parser.core import pp, xml
    tree = xml(lt.tok(open(fn)))
    if show:
        pp(tree)
    N = ns.Name
    import pprint
    print('xmlns', pprint.pformat(N.nss))
    return tree


@click.command()
def samples():
    """Lists the XML provided samples."""
    for sample in os.listdir(SAMPLES):
        print(os.path.sep.join([SAMPLES, sample]))


@click.group()
def cli():
    pass

cli.add_command(samples)
cli.add_command(tree)

if __name__ == '__main__':
    cli()
