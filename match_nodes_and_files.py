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
from document.convert_document import convert_text

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

    file_links = set([Path(l.filepath).stem \
                            for n in link_target_node.descendants \
                            for l in n.links if l.filepath ])

    file_paths = set([f.stem for f in Path(config['file_dir']).iterdir() if f.suffix == '.md'])


    unmatched = [(f, None) for f in file_paths.difference(file_links)]
    unmatched.extend([(None, l) for l in file_links.difference(file_paths)])


    df = pd.DataFrame(unmatched, columns=['File', 'Link'])

    convert_text(df.drop_duplicates().sort_values(['Link', 'File']).to_html(), config['link_report_file'])


if __name__ == '__main__':
    plac.call(main)
