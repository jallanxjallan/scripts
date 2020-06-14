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

sys.path.append('/home/jeremy/Library')

from storage.cherrytree_xml import CherryTree

metadata = dict(doc_separator='date --- location')

def main(config_path, output_file):
    try:
        config = load_config(config_path)
    except Exception as e:
        print(e)
        exit()

    ct = CherryTree(config['content_index'])
    cbn = config['content_base_name']
    content_dir = config['content_dir']

    pandoc_config = {k:v for config.items() if k in pandoc_keys}
    # 'filters':['code_blocks_only'], 'input-files':[], 'output-file':config[]}
    try:
        content_base_node = ct.find_node_by_name(cbn)
    except KeyError:
        print(f'{cbn} not in index')

    input_files = [str(l.filepath) \
                   for n in content_base_node.descendants \
                   for l in  node.links \
                   if content_dir in str(l.filepath)
                   ]


    print(combine_files(pandoc_config, input_files, output-file=output_file)


if __name__ == '__main__':
    plac.call(main)
