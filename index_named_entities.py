#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  extract_content.py
#  

import sys
import re
import csv

from collections import defaultdict

sys.path.append('/home/jeremy/projects/')

from text_processing.extract_content_from_pdf import extract_content
from text_processing.extract_content import extract_named_entities

pdf_source = '/home/jeremy/Documents/one_man_air_force/layouts/Onemanairforce_12_10_2018preview.pdf'

names = 'names.txt'

def main():
    named_entities = defaultdict(set)
    for chunk in [c for p in extract_content(pdf_source) for c in p.text_chunks()]:
        page_no = chunk.text_page_no
        for named_entity in extract_named_entities(chunk.text):
            named_entities[named_entity].add(page_no)
    with open(names, 'w') as outfile:
        for entity in sorted(named_entities):
            pages = ','.join(sorted(named_entities[entity]))
            print(entity, pages, file=outfile)
                
if __name__ == '__main__':
    main()


