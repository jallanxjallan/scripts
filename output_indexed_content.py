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
from utility.config import load_config
from document.pandoc_convert import combine_files


def main(content_index, config_path):
    try:
        config = load_config(config_path)
    except Exception as e:
        print(e)
        exit()

    ct = CherryTree(content_index)
    cbn = config['content_base_name']
    content_dir = config['content_file_dir']
    input_defaults = config['input_args']
    output_defaults = config.get('output_args', {})
    
    try:
        content_base_node = ct.find_node_by_name(cbn)
    except KeyError:
        print(f'{cbn} not in index')

    input_files = [str(l.filepath) \
                   for n in content_base_node.descendants \
                   for l in  n.links \
                   if content_dir in str(l.filepath)
                   ]


    print(combine_files(input_defaults, *input_files, **output_defaults))


if __name__ == '__main__':
    plac.call(main)
