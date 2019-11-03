#!/home/jeremy/ProjectPython/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
# 

import sys 
import os
import re

import lxml.html
from lxml.html import builder as E


sys.path.append('/home/jeremy/library')

from document.text_document import write_document, write_file


ref_docs_dir = '/home/jeremy/Desktop/one_man_air_force/screenplay/book_reference/'
ref_html_dir = '/home/jeremy/Desktop/one_man_air_force/screenplay/html_reference/'
html_index_dir = '/home/jeremy/Desktop/one_man_air_force/screenplay/html_index_docs/'

index_dirs = dict(ev='events', rs='research', ch='characters', bk='background')


def make_index_document(filename, heading):
    try:
        prefix, title = heading.text.split(':')
    except ValueError:
        return False
    hid = heading.attrib['id']
    folder = index_dirs.get(prefix.lower())
    href = 'file://{}#{}'.format(os.path.join(ref_html_dir, filename), hid)
    if not folder:
        print('not a valid prefix')
        return False
    html = E.HTML(
        E.HEAD(
            E.TITLE(title)
            ),
        E.BODY(
            E.H1(title),
            E.P(E.A("link", href=href), "."),
        )
    )
    with open(os.path.join(html_index_dir, folder, hid+'.html'), 'w') as outfile:
        print(lxml.html.tostring(html), file=outfile)
    return True
        
def generate_reference_index():
    for filename in os.listdir(ref_html_dir):
        tree   = lxml.html.parse('file://' + os.path.join(ref_html_dir, filename))
        for heading in tree.xpath('//h1'):
            make_index_document(filename, heading)

def export_reference_docs():
    for filename in os.listdir(ref_docs_dir):
        input_filepath = os.path.join(ref_docs_dir, filename)
        output_filepath =  os.path.join(ref_html_dir, filename).replace('.md', '.html')
        write_file(input_filepath, output_filepath)
        

        
                    
        
if __name__ == "__main__":
    generate_reference_index()
            
     

'''
with open(os.path.join(cooked_dir, filename), 'w') as outfile:
            lines = [l.strip() for l in open(os.path.join(raw_dir, filename)).readlines()]
            curr_para = 0
    
            for i in range(len(lines)):
                if re.match(r'==', lines[i]):
                    print('#', lines[i-1], file=outfile)
                    curr_para = i
                elif re.match(r'--', lines[i]):
                    print('##', lines[i-1], file=outfile)
                    curr_para = i
                elif not lines[i].strip():
                    if lines[i-1].endswith(('.', '?', '!', '"')):
                        print(' '.join([l for l in lines[curr_para:i]]), file=outfile)
                        print('', file=outfile)
                        curr_para = i + 1
                    else:
                        lines[i] = '-'
                elif i == len(lines) -1:
                    print(' '.join([l for l in lines[curr_para:i+1]]), file=outfile)
'''
