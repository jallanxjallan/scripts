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

split_pat = r'\={:4}+'

def import_document(source_file, target_dir, filename_template):
    filters = ['inline_notes.lua', 'split_document_on_heading.lua']
    sectioned = pypandoc.convert_file(source_file, 'markdown', lua-filters=filters)
    for no, content in enumerate(re.split(split_pat, sectioned)):
        print(content[:30])
        # identifier = sections[sindex]
        # content = sections[sindex+ 1]
        #
        # outfile = Path(target_dir, f'{filename_template}_{section_number}').with_suffix('.md')
        #
        # args = [f'--defaults=create_document.yaml',
        #         f'--metadata=title:{identifier.replace("-"," ").title()}'
        #         ]
        # pypandoc.convert_text(content,
        #                       'markdown',
        #                       format='markdown',
        #                       outputfile=str(outfile),
        #                       extra_args=args)
        # section_number += 10

if __name__ == '__main__':
    fire.Fire(import_document)
