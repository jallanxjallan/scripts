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

def format_metadata(target, prefix):
    with open('create_document.yaml') as infile:
        defaults = yaml.load(infile)

    for doc_key in sys.stdin.read().split("\n"):
        print(doc_key)


        # identifier, content = section
        # filename = f'{prefix}_{identifier}'
        # metadata = defaults['metadata']
        # metadata['sequence'] = no
        # metadata['title'] = identifier.replace('-', ' ').title()
        #
        # outputfile = Path(Path.cwd(), target, filename).with_suffix('.md')
        #
        # with outputfile.open('a') as outfile:
        #     print('---', file=outfile)
        #     yaml.dump(metadata, outfile)
        #     print('---', file=outfile)
        #     print(content, file=outfile)

if __name__ == '__main__':
    fire.Fire(format_metadata)
