#!/home/jeremy/Scripts/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import attr

import pypandoc
from ruamel.yaml import YAML

MARKDOWN = 'markdown_mmd+yaml_metadata_block'
yaml=YAML(typ='safe') 




@attr.s
class Document():
    source = attr.ib()
    meta = attr.ib(factory=dict)
    
    def __attrs_post_init__(self):
        if self.source.__class__.__name__ is 'PosixPath':
            if self.source.suffix in ('.md', '.txt'):
                text = self.source.read_text()
                try: 
                    meta, text = text.split('---')[1:]
                except IndexError:
                    meta = {}
                except ValueError:
                    meta = {}
                self.text = text
                if len(meta) > 0:
                    self.meta = yaml.load(meta)
            else:
                self.text = pypandoc.convert_file(str(self.source), to='markdown')
        elif  fp.__class__.__name__ is str:
                self.text = pypandoc.convert_text(self.source, to='markdown')
        else:
            raise 'Unknown source'
    
    def __str__(self):
        return self.text
        
    def write_document(self, filepath):
        args = [f'--metadata={k}:{v}' for k,v in self.meta.items()]
        args.append('--standalone')
        pypandoc.convert_text(self.text,
            format=MARKDOWN, 
            to=MARKDOWN,
            outputfile=str(filepath),
            extra_args=args
        )
            
    
        
'''
def output_document(self, outputfile):
        
    
    def read_from_text(self):
        self.text = convert_file(self.source)
        self.meta = yaml.load(self.source.read_text())
        
    
    
        
        
    def input_document(self
    
    def convert_file(filepath):
    try:
        return pypandoc.convert_file(str(filepath), MARKDOWN)
    except FileNotFoundError:
        logger.info(f'unable to import {filepath}')
        return False
        
def convert_text(text):
    try:
        return pypandoc.convert_text(str(filepath), MARKDOWN)
    except FileNotFoundError:
        logger.info(f'unable to import {filepath}')
        return False
        

'''
        
    
    
