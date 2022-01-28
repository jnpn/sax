from nose.tools import assert_equal, assert_not_equal
import io
from sax.tokenizer.interface import opening, closing, selfclosing, \
    text, comment, doctype, instruction, error
from sax.tokenizer.loop import tok, peek

'''

src = './samples/dbus-systemd1.xml'

tsg = list(gt.tok(open(src)))
tsl = list(lt.tok(open(src)))


def k(n=32):
    for k, t in tsl[:n]:
        print(k, t)


diffs = [(g, l) for g, l in zip(tsg, tsl) if g != l]

'''

'''
Intersting, parsers have different streams. Mostly out of
sync because of the selfclosing `tokenistic sugar` trick,
causing more tokens emitted by gen.tok:

<sctag/> -> (opening, sctag), (closing, sctag)

instead of

<sctag/> -> (selfclosing, sctag)

but may resolve the same trees when parsed.
'''



def test_peek():
    bnil = ''
    bsnil = io.StringIO(bnil)
    assert_equal(bnil, peek(bsnil))


def test_peek0():
    c = peek(io.StringIO('<foo>'), off=2)
    e = 'f'
    assert_equal(c, e)


def test_peek1():
    c = peek(io.StringIO('<foo>'), off=3)
    e = 'o'
    assert_equal(c, e)


# def test_peek_span():
#     bs = io.StringIO('aBcDeF')
#     assert_equal(peek(bs, off=2), 'B')
#     assert_equal(peek(bs, off=2), 'B')
#     assert_not_equal(peek(bs, off=2, span=2), 'BcD')
#     assert_equal(peek(bs, off=2, span=2), 'Bc')


def test_peek_above_left():
    return assert_equal(peek(io.StringIO('<foo>'), off=6), '>')


def test_empty_text():
    t = list(tok(io.StringIO('')))
    e = []
    assert_equal(t, e)


def test_tok_text():
    e = [(text, 'foo')]
    t = list(tok(io.StringIO('foo')))
    assert_equal(t, e)


def test_tok_opening():
    e = [(opening, '<foo>')]
    t = list(tok(io.StringIO('<foo>')))
    assert_equal(t, e)


def test_tok_instruction():
    e = [(instruction, '<?foo?>')]
    t = list(tok(io.StringIO('<?foo?>')))
    assert_equal(t, e)


def test_tok_error_comment():
    e = [(error, '<!--foo>')]
    t = list(tok(io.StringIO('<!--foo>')))
    assert_equal(t, e)


def test_tok_error_instruction():
    e = [(error, '<?instruction>')]
    t = list(tok(io.StringIO('<?instruction>')))
    assert_equal(t, e)


def test_tok_doctype():
    e = [(doctype, '<!doctype>')]
    t = list(tok(io.StringIO('<!doctype>')))
    assert_equal(t, e)


def test_tok_selfclosing():
    e = [(selfclosing, '<foo/>')]
    t = list(tok(io.StringIO('<foo/>')))
    assert_equal(t, e)


def test_text_opening():
    bs = 'text<foo>'
    t = list(tok(io.StringIO(bs)))
    e = [(text, 'text'),
         (opening, '<foo>')]
    assert_equal(t, e)


def test_opening():
    bs = '<foo>'
    i = list(tok(io.StringIO(bs)))
    e = [(opening, '<foo>')]
    assert_equal(i, e)


def test_opening_closing():
    bs = '<foo></foo>'
    i = list(tok(io.StringIO(bs)))
    e = [(opening, '<foo>'),
         (closing, '</foo>')]
    assert_equal(i, e)


def test_opening_opening():
    bs = '<foo><bar>'
    i = list(tok(io.StringIO(bs)))
    e = [(opening, '<foo>'),
         (opening, '<bar>')]
    assert_equal(i, e)


def test_opening_attrs():
    bs = '<foo a="a" b="b">'
    i = list(tok(io.StringIO(bs)))
    e = [(opening, '<foo a="a" b="b">')]
    assert_equal(i, e)


def test_closing():
    bs = '</foo>'
    i = list(tok(io.StringIO(bs)))
    e = [(closing, '</foo>')]
    assert_equal(i, e)

def test_selfclosing():
    bs = '<foo/>'
    i = list(tok(io.StringIO(bs)))
    e = [(selfclosing, '<foo/>')]
    assert_equal(i, e)


def test_instruction_too_short():
    bs = '<?xml version="1.0" encoding="UTF-8"?'
    i = list(tok(io.StringIO(bs)))
    e = [(error, '<?xml version="1.0" encoding="UTF-8"?')]
    assert_equal(i, e)


def test_instruction():
    bs = '<?xml version="1.0" encoding="UTF-8"?>'
    i = list(tok(io.StringIO(bs)))
    e = [(instruction, '<?xml version="1.0" encoding="UTF-8"?>')]
    assert_equal(i, e)


def test_instruction_2():
    bs = '<?xml version="1.0" encoding="UTF-8"?><?instruction?>'
    i = list(tok(io.StringIO(bs)))
    e = [(instruction, '<?xml version="1.0" encoding="UTF-8"?>'),
         (instruction, '<?instruction?>')]
    assert_equal(i, e)


def test_instruction_text():
    bs = '<?xml version="1.0" encoding="UTF-8"?>text'
    i = list(tok(io.StringIO(bs)))
    e = [(instruction, '<?xml version="1.0" encoding="UTF-8"?>'),
         (text, 'text')]
    assert_equal(i, e)


def test_text_opening_text_closing():
    bs = 'eww<foo>bar</foo>'
    i = list(tok(io.StringIO(bs)))
    e = [(text, 'eww'),
         (opening, '<foo>'),
         (text, 'bar'),
         (closing, '</foo>')]
    assert_equal(i, e)


def test_opening_text_closing():
    bs = '<foo>bar</foo>'
    i = list(tok(io.StringIO(bs)))
    e = [(opening, '<foo>'),
         (text, 'bar'),
         (closing, '</foo>')]
    assert_equal(i, e)


def test_instruction_text_instruction():
    bs = '<?xml version="1.0" encoding="UTF-8"?>text<?instruction?>'
    i = list(tok(io.StringIO(bs)))
    e = [(instruction, '<?xml version="1.0" encoding="UTF-8"?>'),
         (text, 'text'),
         (instruction, '<?instruction?>')]
    assert_equal(i, e)
