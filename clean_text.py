#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  clean_text.py
#  
#  Copyright 2018 Jeremy Allan <jeremy@jeremy-Latitude-E6220>
#  

import sys
import re
import json

input_file = 'reference_text.json'
output_file = 'reference.md'

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
            
    


if __name__ == '__main__':
    main()
