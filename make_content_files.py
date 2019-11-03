#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys 
import os
import re
from pathlib import Path
#~ import pandas as pd
import plac
from bs4 import BeautifulSoup

sys.path.append('/home/jeremy/Library/')

from document.text_document import read_document, write_document


fname_pat = re.compile('(\d+)\s(.+)')

def main(content_source, dispatch_dir):
    fnc = Path(content_source)

    content = read_document(str(fnc)).split('|')
    for i in range(0, len(content), 2):
        slugline = BeautifulSoup(content[i], 'lxml')
        
        m = fname_pat.search(slugline.get_text(), re.I)
        if not m:
            continue
        page_no = m.group(1)
        desc = re.sub("\W", "", m.group(2)).lower().replace(' ', '_')
        filename = f'page_{page_no}_{fnc.stem}_{desc}'
        item = content[i+1].replace('=', '')
        
        filepath = Path(dispatch_dir, filename).with_suffix('.md')
        
        write_document(item, filepath)
        
        

if __name__ == '__main__':
    plac.call(main)
    
