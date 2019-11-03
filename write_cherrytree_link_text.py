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
    

def write_cherrytree_node_text(filepath, outputfile, root_node=None):
    with CherryTree(db, 'Scenes') as ct:
        content = [extract_link_text(n) for n in ct.root_node.children]
        if len(content) > 0:
            text_to_file(content, outputfile)

if __name__ == '__main__':
    plac.call(write_cherrytree_node_text)
    
