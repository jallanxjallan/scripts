#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys 
import os
from pathlib import Path
from lxml import etree
from lxml.etree import XMLSyntaxError
import pypandoc



icml_source_dir = '/home/jeremy/Desktop/cergam/exported_content'
edit_file = '/home/jeremy/Desktop/cergam/final_text/captions.odt'

xpat = './/ParagraphStyleRange[@AppliedParagraphStyle="ParagraphStyle/Caption"]//Content'


def main():
    contents = []
    for filename in os.listdir(icml_source_dir):
        captions = []
        try:
            tree = etree.parse(os.path.join(icml_source_dir, filename))
        except XMLSyntaxError:
            continue
        for e in tree.findall(xpat):
            if len(e.text) > 5: 
                captions.append(e.text)
        if len(captions) > 0:
            contents.extend(captions)
            contents.append('-' * 20)
        
    pypandoc.convert_text('\n\n'.join(contents), 'odt', format='markdown_mmd', outputfile=edit_file)
    
    

if __name__ == '__main__':
    main()
    
