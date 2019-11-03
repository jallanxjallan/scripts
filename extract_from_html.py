#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys 
import os
from pathlib import Path
from bs4 import BeautifulSoup
import re

sys.path.append('/home/jeremy/Library/')

html_source = '/home/jeremy/Desktop/cergam/extracted_text.html'
text_dir = '/home/jeremy/Desktop/cergam/final_text/'


def main():
    html = Path(html_source)
    soup = BeautifulSoup(html.read_text(), 'lxml')
    for div in soup.find_all('div'):
        print(div)
    
        #~ Path(dest_dir, chapter_filename).write_text('\n'.join(content))  


if __name__ == '__main__':
    main()
