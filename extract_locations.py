#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  extract_content.py
#  

import sys
import re
import csv

from collections import defaultdict

sys.path.append('/home/jeremy/projects/text_processing')

from extract_content_from_pdf import extract_content
from extract_named_entities import extract_named_entities

pdf_source = 'Onemanairforce_12_10_2018preview.pdf'

names = 'names.txt'

def main():
    named_entities = defaultdict(list)
    for chunk in [c for p in extract_content(pdf_source) for c in p.text_chunks()]:
        for named_entity in extract_named_entities(chunk.text):
            named_entities[named_entity].append(chunk.pdf_page)
            
    with open(names, 'w') as outfile:
        for entity in sorted(named_entities):
            pages = ','.join(named_entities[name])
            print(entity, pages, file=outfile)
                
if __name__ == '__main__':
    main()


