#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys 
import os
from collections import namedtuple, defaultdict

sys.path.append('/home/jeremy/Library/')

from language.parse_labelled_text import parse_labelled_text
from data_storage.cherrytree import CherryTree
from document.text_document import render_document, write_document
from utility.config import load_config_from_filepath
from utility.helpers import snake_case



def load_content(config):
    ct = CherryTree(config.database)
    
    content = {}
    
    
    for node in ct.select_nodes():
        
        labelled_text_items = [l for l in parse_labelled_text(node.text,config.labels)]
        content_item = {t.label:t.text for t in labelled_text_items if not t.label == 'text'}
        text_content = '|'.join([t.text for t in labelled_text_items if t.label == 'text' if len(t.text.strip()) > 0])
        if len(text_content) > 0:
            content_item['text'] = text_content
        content_item = namedtuple('ContentItem', content_item)(**content_item)
        if len(content_item)== 0:
            continue
        
        ancestors = node.ancestry
        if ancestors:
            try:
                content[snake_case(ancestors[0].name)].append(content_item)
            except Exception as e:
                content[snake_case(ancestors[0].name)] = [content_item]
        else:
            content[snake_case(node.name)] = content_item
    return content
    
def print_resume(config_filepath):

    config = load_config_from_filepath(config_filepath)
    
    content = load_content(config)
    document = render_document(config.template, content)
    filepath = '/home/jeremy/Desktop/layla_resume10.odt'
    #~ with open(filepath, 'w') as outfile:
        #~ outfile.write(document)
    return write_document(document, filepath, input_format='html')
    
