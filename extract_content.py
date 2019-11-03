#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  extract_content.py
#  

import sys
import re
import nltk

sys.path.append('/home/jeremy/Apps/textprocessor')

from extract_pdf_content import extract_content

pdf_source = 'Onemanairforce_12_10_2018preview.pdf'

output_file = 'reference_text2.md'

chapter_pat = re.compile(r'\d*\s[A-Z]')
number_pat = re.compile(r'\d\s\d')


def main():
    with open(input_file) as infile:
        contents = json.load(infile)
        
    with open(output_file, 'w') as outfile:
        lines = []
        i = 0
        while i < len(contents):
            if chapter_pat.match(contents[i][1]):
                print(' '.join(lines), file=outfile)
                lines = []
                lines.append('#' + contents[i][1])
                lines.append('##'+ contents[i+1][1])
                i += 2
                
            else:
                if not number_pat.match(contents[i]):
                    lines.append(contents[i])
            i +=1
        print(' '.join(lines), file=outfile)


def main():
    for obj in [o for p in extract_content(pdf_source) for o in p.objects]:
        
        
    with open(output_file, 'w') as outfile:
        json.dump(output, outfile)
                

if __name__ == '__main__':
    main()


