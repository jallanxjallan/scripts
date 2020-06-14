#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import plac
from pathlib import Path
import yaml
import pandas as pd

sys.path.append('/home/jeremy/Library')

from storage.cherrytree_xml import CherryTree
from document.convert_document import convert_file
from utility.helpers import snake_case

filter_path = Path('/home/jeremy/Library/document/filters')

def main(config_path):

    cpath = Path(config_path)
    if not cpath.exists():
        print('no config found')
        exit()
    config = yaml.load(cpath.read_text())

    ct = CherryTree(config['source_index'])

    link_target_node = ct.find_node_by_name(config['target_name'])
    if not link_target_node:
        print(f'target node {target_name} not found')
        exit()

    output_args = config['output_args']
    for filepath in [str(l.filepath)
             for n in link_target_node.descendants
             for l in n.links if l.filepath ]:
        convert_file(filepath, **output_args)

    print('finished')


if __name__ == '__main__':
    plac.call(main)
