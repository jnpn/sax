import sys
import io

from nose.tools import assert_equal, raises, assert_not_equal

from saxg import root
from parserg import Root, Comment, Doctype, Text, Inst, Tag, MalformedXML, xml


sys.setrecursionlimit(1750)


def strcopy(buf):
    '''vestigial code'''
    s = buf.read()
    buf.seek(0)
    return s


def test_0():
    s = io.BytesIO(b'<foo>x</foo>')
    # print(strcopy(s))
    t = xml(root(s))
    # return t
    e = Root([Tag(b'<foo>', [], [Text(b'x')])])
    assert_equal(t, e)


def test_1():
    '''bug'''
    s = io.BytesIO(b'<foo><bar>duh</bar></foo>')
    # print(strcopy(s))
    t = xml(root(s))
    # return t
    e = Root([Tag(b'<foo>', [], [Tag(b'<bar>', [], [Text(b'duh')])])])
    assert_equal(t, e)


def test_xml():
    s = open('./samples/dbus.xml', 'rb')
    # print(strcopy(s))
    # return xml(root(s))
    t = xml(root(s))
    e = Root(children=[Inst(inst=b'<?xml version="1.0"?>'), Text(text=b' '), Comment(comment=b'<!--*-nxml-*-->'), Text(text=b'\n'), Doctype(doctype=b'<!DOCTYPE busconfig PUBLIC "-//freedesktop//DTD D-BUS Bus Configuration 1.0//EN"\n        "http://www.freedesktop.org/standards/dbus/1.0/busconfig.dtd">'), Text(text=b'\n\n'), Comment(comment=b'<!--\n  This file is part of systemd.\n\n  systemd is free software; you can redistribute it and/or modify it\n  under the terms of the GNU Lesser General Public License as published by\n  the Free Software Foundation; either version 2.1 of the License, or\n  (at your option) any later version.\n-->'), Text(text=b'\n\n'), Tag(name=b'<busconfig>', attrs=[], children=[Text(text=b'\n\n        '), Tag(name=b'<policy user="root">', attrs=[], children=[Text(text=b'\n                '), Tag(name=b'<allow own="org.freedesktop.timedate1"/>', attrs=[], children=[]), Text(text=b'\n                '), Tag(name=b'<allow send_destination="org.freedesktop.timedate1"/>', attrs=[], children=[]), Text(text=b'\n                '), Tag(name=b'<allow receive_sender="org.freedesktop.timedate1"/>', attrs=[], children=[]), Text(text=b'\n        ')]), Text(text=b'\n\n        '), Tag(name=b'<policy context="default">', attrs=[], children=[Text(text=b'\n                '), Tag(name=b'<allow send_destination="org.freedesktop.timedate1"/>', attrs=[], children=[]), Text(text=b'\n                '), Tag(name=b'<allow receive_sender="org.freedesktop.timedate1"/>', attrs=[], children=[]), Text(text=b'\n        ')]), Text(text=b'\n\n')]), Text(text=b'\n')])
    assert_equal(t, e)


def test_xml_cv():
    s = open('./samples/cv.xml', 'rb')
    # print(strcopy(s))
    # return xml(root(s))
    t = len(xml(root(s)).children)
    e = None
    assert_not_equal(t, e)


def test_pp():
    '''
    pp(Root([Tag('foo',[],[Inst('doctype'),
                           Text('wat'),
                           Tag('bar', [], [Text('duh')])])]))
    ->
    Root
    foo
    Inst doctype
    Text wat
    bar
    Text duh
    # OK
    '''
    pass


@raises(AssertionError, MalformedXML)
def test_malformed():
    s = io.BytesIO(b'<foo><bar>xxx</foo></bar>')
    try:
        t = xml(root(s))
    except MalformedXML:
        pass
