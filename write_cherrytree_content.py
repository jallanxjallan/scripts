#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys 
import os
from collections import namedtuple
from pathlib import Path

import plac

sys.path.append('/home/jeremy/Library/')

from data_storage.cherrytree import CherryTree
from document.text_document import text_to_file

def extract_link_text(node):
     for link in node.links:
        if link.type == 'file':
            yield Path(link.value).read_text()
    
def extract_node_text(node):
    if node.text:
        yield node.text 

def write_cherrytree_content(filepath, outputfile, node=None, text=False, links=True):
    with CherryTree(db, node) as ct:
        content = []
        for node in ct.root_node.children:
        if text:
            content.extend(filter(None, [t for t in extract_node_text(n)])
        if links:
            content.extend([t for n in ct.root_node.children] for t in extract_link_text(n))
        if len(content) > 0:
            text_to_file(content, outputfile)

if __name__ == '__main__':
    plac.call(write_cherrytree_link_text)
    
