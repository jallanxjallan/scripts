#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import fire
from pathlib import Path
import sys
import re
from ruamel.yaml import YAML

yaml = YAML()

pat = re.compile('\W+((\w|\-)+)\s\.section\W')

def write_document_sections(target, prefix):
    with open('create_document.yaml') as infile:
        defaults = yaml.load(infile)

    text = sys.stdin.read()

    s = re.split(pat, text)
    sections = [(s[i], s[i+2]) for i in range(1,len(s)-1, 3)]

    for no, section in enumerate(sections):
        identifier, content = section
        filename = f'{prefix}_{identifier}'
        metadata = defaults['metadata']
        metadata['sequence'] = no
        metadata['title'] = identifier.replace('-', ' ').title()

        outputfile = Path(Path.cwd(), target, filename).with_suffix('.md')

        with outputfile.open('a') as outfile:
            print('---', file=outfile)
            yaml.dump(metadata, outfile)
            print('---', file=outfile)
            print(content, file=outfile)

if __name__ == '__main__':
    fire.Fire(write_document_sections)
