#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
from pathlib import Path
import plac

import pandas as pd

import pypandoc

def set_replace_string(key, value):
    if value == 'ital':
        value = f'*{key}*'
    return str(value)

def make_term_map(df, old, new, index):
    mapping = df.set_index(old).T.to_dict(new)
    return {k:set_replace_string(k,v) for k,v in mapping.items()} 
        
def main(termfile, infile):
    words = pd.read_excel(termfile, sheet_name='words').dropna()
    entities = pd.read_excel(termfile, sheet_name='entities').dropna()
    fn = Path(infile)
    
    content = pypandoc.convert_file(infile, to='markdown_mmd')
    for old, new in make_term_map(words, 'word', 'replace', 1).items():
        print(old, new)
        try:
            content = content.replace(old, new)
        except:
            continue
    
    for old, new in make_term_map(entities, 'entity', 'replace', 2).items():
        print(old, new)
        try:
            content = content.replace(old, new)
        except:
            continue
        
    outfile = Path(fn).with_name(f'{fn.stem}_corrected{fn.suffix}')
    rs = pypandoc.convert_text(content, to='odt', format='markdown_mmd', outputfile=str(outfile))
    print(rs)
    
    
if __name__ == '__main__':
    plac.call(main)
