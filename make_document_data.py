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

def document_data(target, prefix):
    with open('create_document.yaml') as infile:
        defaults = yaml.load(infile)

    rkey in sys.stdin.read().split("\n")
    doc_data = r.hgetall(rkey)



        # filename = f'{prefix}_{identifier}'
        # metadata = defaults['metadata']
        # metadata['sequence'] = no
        # metadata['title'] = identifier.replace('-', ' ').title()
        #
        # outputfile = Path(Path.cwd(), target, filename).with_suffix('.md')



if __name__ == '__main__':
    fire.Fire(create_documents)
