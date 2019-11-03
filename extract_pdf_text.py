#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys 
import os
from collections import namedtuple
from pathlib import Path
from uuid import uuid4

import plac
from textacy.preprocessing.normalize import normalize_hyphenated_words, normalize_quotation_marks, normalize_whitespace

sys.path.append('/home/jeremy/Library/')

from redisdb import RedisDB

from document.pdf_document import parse_pdf_document


r = RedisDB()

def extract_from_pdf(pdf_source, text_folder):
    pdf = Path(pdf_source)
    text_dir = Path(text_folder)
    if not text_dir.exists():
        text_dir.mkdir()
    
    for page, tbox in [(p,b) for p in parse_pdf_document(pdf_source) for b in p.text_boxes]:
        component_uid = uuid4().hex
        uri = Path(text_dir, component_uid).with_suffix('.md').as_uri()
        uri.write_text(tbox.text)
        r.
        
        
        
            
            filepath = write_text_to_file(tbox.text, text_dir)
            store_meta_to_redis(page, tbox, filepath)
        
        
    
if __name__ == '__main__':
    plac.call(extract_from_pdf)
    
