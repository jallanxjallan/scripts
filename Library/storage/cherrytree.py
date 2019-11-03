#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cherrytree.py
#  

import sys
import os
import re
from collections import namedtuple, defaultdict
from pathlib import Path
import base64
import logging

from lxml import etree

logger = logging.getLogger(__name__)

UNCHECKEDBOX = "☐"
CHECKEDBOX = "☑"

Link = namedtuple('Link', ('label, type, url'))
Formatted = namedtuple('Formatted', ('tag text'))

from peewee import *

database = SqliteDatabase(None, **{})

class UnknownField(object):
    def __init__(self, *_, **__): pass
    

#~ class CheckList():
    #~ def __init__(self, checklist):
        #~ self.checklist = checklist
    #~ @property
    #~ def todos(self):
        #~ todos = {}
        #~ for line in [l for c in self.node if c.tag == 'rich_text' if c.text for l in c.text.split("\n")]:
            #~ if line.startswith(UNCHECKEDBOX):
                #~ todos[line.strip(UNCHECKEDBOX).lstrip()] = 0
            #~ elif line.startswith(CHECKEDBOX):
                #~ todos[line.strip(CHECKEDBOX).lstrip()] = 1
        #~ return todos


class RichTextField(Field):
    field_type = 'TEXT'
    
    def db_value(self, value):
        return str(value) # convert object into string.

    def python_value(self, xml):
        return etree.fromstring(xml) # convert to lxml object


class BaseModel(Model):
    class Meta:
        database = database

class Bookmark(BaseModel):
    node = IntegerField(column_name='node_id', null=True, unique=True)
    sequence = IntegerField(null=True)

    class Meta:
        table_name = 'bookmark'
        primary_key = False

class Children(BaseModel):
    father = IntegerField(column_name='father_id', null=True)
    node = IntegerField(column_name='node_id', null=True, unique=True)
    sequence = IntegerField(null=True)

    class Meta:
        table_name = 'children'
        primary_key = False

class Codebox(BaseModel):
    do_highl_bra = IntegerField(null=True)
    do_show_linenum = IntegerField(null=True)
    height = IntegerField(null=True)
    is_width_pix = IntegerField(null=True)
    justification = TextField(null=True)
    node = IntegerField(column_name='node_id', null=True)
    offset = IntegerField(null=True)
    syntax = TextField(null=True)
    txt = RichTextField(null=True)
    width = IntegerField(null=True)

    class Meta:
        table_name = 'codebox'
        primary_key = False

class Grid(BaseModel):
    col_max = IntegerField(null=True)
    col_min = IntegerField(null=True)
    justification = TextField(null=True)
    node = IntegerField(column_name='node_id', null=True)
    offset = IntegerField(null=True)
    txt = TextField(null=True)

    class Meta:
        table_name = 'grid'
        primary_key = False

class Image(BaseModel):
    anchor = TextField(null=True)
    filename = TextField(null=True)
    justification = TextField(null=True)
    link = TextField(null=True)
    node = IntegerField(column_name='node_id', null=True)
    offset = IntegerField(null=True)
    png = BlobField(null=True)
    time = IntegerField(null=True)

    class Meta:
        table_name = 'image'
        primary_key = False

class Node(BaseModel):
    has_codebox = IntegerField(null=True)
    has_image = IntegerField(null=True)
    has_table = IntegerField(null=True)
    is_richtxt = IntegerField(null=True, default=True)
    is_ro = IntegerField(null=True, default=False)
    level = IntegerField(null=True)
    name = TextField()
    node = IntegerField(column_name='node_id', null=True, unique=True)
    syntax = TextField(null=True)
    tags = TextField(null=True)
    txt = RichTextField(null=True)
    
    @property
    def parent(self):
        father = Children.get(Children.node == self.node)
        try:
            return Node.get(Node.node == father.father)
        except:
            return None

    @property
    def ancestors(self):
        #~ print('node name', self.name)
        ans = [self]
        while True:
            parent = ans[0].parent
            if parent:
                ans.insert(0, parent)
            else:
                break
        return ans
    
    
    @property
    def children(self):
        for node in Node.select().join(Children, on=(Node.node == Children.node)).where(Children.father == self.node).order_by(Children.sequence):
            yield node
    
    @property
    def siblings(self):
        for node in Node.select().join(Children, on=(Node.node == Children.node)).where(Children.father == self.parent.node).order_by(Children.sequence):
            if not node.node== self.node:
                yield node
                
    @property
    def text(self):
        return ('\n').join([l.strip() for l in ''.join(self.txt.itertext()).split('\n') if len(l.strip()) > 0])
        
        
    @property
    def links(self):
        for link in [l for l in self.txt.iter('rich_text') if 'link' in l.attrib]:
            key, value = link.attrib['link'].split()
            if key == 'file':
                value = base64.b64decode(value).decode()
            yield Link(link.text, key, value)
    
    @property
    def formatted_text(self):
        for line in [l for l in self.txt.iter('rich_text') if 'scale' in l.attrib]:
            yield Formatted(line.attrib['scale'], line.text)

    
    @property
    def sequence(self):
        return Children.get(Children.node == self.node).sequence
    
    class Meta:
        table_name = 'node'
        primary_key = False

class KeyValue(BaseModel):
    key = TextField()
    value = TextField()
    node = ForeignKeyField(Node, field='node', column_name='node_id')
    
    class Meta:
        table_name = 'key_value'
        primary_key = False

class CherryTree():
    def __init__(self, filepath, root_node=0):
        fp = Path(filepath)
        if not fp.exists():
            raise FileNotFoundError
        self.db = database
        self.db.init(filepath)
        self.db.connect()
        try:
            self.root_node = self.find_node(root_node)
        except IndexError:
            print(f'{root_node} does not exist')
            
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.db.close()

    def find_node(self, arg):
        if type(arg) is int:
            return Node.get(arg)
        names = arg.split('/')
        node = Node.get(Node.name == names.pop(0))
        for name in names:
            node = next((c for c in node.children if c.name == name), None)
            if not node:
                break
        return node
                
    def select_nodes(self):
        for node in Node.select():
                yield node
    
    def select_top_nodes(self):
        for node in Node.select().join(Children, on=(Node.node == Children.node)).where(Children.father == 0):
            yield node
