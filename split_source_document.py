#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import fire
from pathlib import Path
import re
import pypandoc
import uuid

split_pat = r'qqq(\w+(?:-\w+)+)xxx'

def split_document(source_file, target_dir, filename_template):

    marked = pypandoc.convert_file(source_file, 'markdown', filters=['set_split_pattern.py'])
    sections = re.split(split_pat, marked)
    section_number = 100
    for sindex in range(1, len(sections), 2):
        identifier = sections[sindex]
        content = sections[sindex+ 1]

        outfile = Path(target_dir, f'{filename_template}_{section_number}').with_suffix('.md')

        args = [f'--defaults=create_document.yaml',
                f'--metadata=title:{identifier.replace("-"," ").title()}'
                ]
        pypandoc.convert_text(content,
                              'markdown',
                              format='markdown',
                              outputfile=str(outfile),
                              extra_args=args)
        section_number += 10

if __name__ == '__main__':
    fire.Fire(split_document)
