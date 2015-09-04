import io

from nose.tools import assert_equal, raises, assert_not_equal

from sax.tokenizer.gen import tok
from sax.parser.interface import Root, Comment, Doctype, Text, Instruction, \
    Tag
from sax.parser.core import xml
from sax.parser.exceptions import MalformedXML


def test_0():
    s = io.StringIO('<foo>x</foo>')
    t = xml(tok(s))
    e = Root([Tag('<foo>', [], [Text('x')])])
    assert_equal(t, e)


def test_1():
    '''bug'''
    s = io.StringIO('<foo><bar>duh</bar></foo>')
    t = xml(tok(s))
    e = Root([Tag('<foo>', [], [Tag('<bar>', [], [Text('duh')])])])
    assert_equal(t, e)


def test_xml():
    s = open('./samples/dbus.xml')
    t = xml(tok(s))

    e = Root(children=[
        Instruction(instruction='<?xml version="1.0"?>'), Text(text=' '),
        Comment(comment='<!--*-nxml-*-->'), Text(text='\n'), Doctype(
            doctype='<!DOCTYPE busconfig PUBLIC "-//freedesktop//DTD D-BUS '
            'Bus Configuration 1.0//EN"\n        "http://www.freedesktop.org/'
            'standards/dbus/1.0/busconfig.dtd">'),
        Text(text='\n\n'),
        Comment(comment='<!--\n  This file is part of systemd.\n\n  systemd '
                'is free software; you can redistribute it and/or modify '
                'it\n  under the terms of the GNU Lesser General Public '
                'License as published by\n  the Free Software Foundation; '
                'either version 2.1 of the License, or\n  (at your option) '
                'any later version.\n-->'),
        Text(text='\n\n'),
        Tag(name='<busconfig>',
            attrs=[],
            children=[
                Text(text='\n\n        '),
                Tag(
                    name='<policy user="root">',
                    attrs=[],
                    children=[Text(text='\n                '),
                              Tag(
                                  name='<allow own="org.freedesktop.'
                                  'timedate1"/>',
                                  attrs=[],
                                  children=[]),
                              Text(text='\n                '),
                              Tag(
                                  name='<allow send_destination="org.'
                                  'freedesktop.timedate1"/>',
                                  attrs=[],
                                  children=[]),
                              Text(text='\n                '),
                              Tag(
                                  name='<allow receive_sender="org.'
                                  'freedesktop.timedate1"/>',
                                  attrs=[],
                                  children=[]),
                              Text(text='\n        ')]),
                Text(text='\n\n        '),
                Tag(
                    name='<policy context="default">',
                    attrs=[],
                    children=[Text(text='\n                '),
                              Tag(
                                  name='<allow send_destination="'
                                  'org.freedesktop.timedate1"/>',
                                  attrs=[],
                                  children=[]),
                              Text(text='\n                '),
                              Tag(
                                  name='<allow receive_sender="org.'
                                  'freedesktop.timedate1"/>',
                                  attrs=[],
                                  children=[]),
                              Text(text='\n        ')]),
                Text(text='\n\n')]),
        Text(text='\n')])
    assert_equal(t, e)


def test_xml_cv():
    s = open('./samples/cv.xml')
    t = len(xml(tok(s)).children)
    e = None
    assert_not_equal(t, e)


def test_pp():
    '''
    pp(Root([Tag('foo',[],[Instruction('doctype'),
                           Text('wat'),
                           Tag('bar', [], [Text('duh')])])]))
    ->
    Root
    foo
    Instruction doctype
    Text wat
    bar
    Text duh
    # OK
    '''
    pass


@raises(AssertionError, MalformedXML)
def test_malformed():
    s = io.StringIO('<foo><bar>xxx</foo></bar>')
    try:
        t = xml(tok(s))
    except MalformedXML:
        pass
