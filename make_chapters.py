#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys 
import os
from pathlib import Path
import csv
import re

sys.path.append('/home/jeremy/Library/')

source_dir = '/home/jeremy/Desktop/cergam/pre_edited_text/'
dest_dir = '/home/jeremy/Desktop/cergam/chapters/'





def main():
    chapter_list = csv.DictReader(Path('chapter_list.csv').open())
    for chapter in chapter_list:
        content = []
        chapter_filename = f'{chapter["Chapter"].lower().replace(" ", "_")}.md'
        for i in range(int(chapter['Start']), int(chapter['End']) + 1):
            text = Path(source_dir, f'cergam_initial_page_{i}.md').read_text()
            if re.search('original text|first edit|reedit|dispatched', text):
                content.append('+' * 30)
                content.append(f'###The following text was extracted From CERGAM 20190828.pdf page {str(i)}')
                content.append(text.split('...')[1])
        Path(dest_dir, chapter_filename).write_text('\n'.join(content))  


#~ if __name__ == '__main__':
    #~ main()
