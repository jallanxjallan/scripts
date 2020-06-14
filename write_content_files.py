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
from utility.config import load_config

def main(config):
    """Match files in target directory with nodes containing file link
    config fields: content_index, content_base_name, content_file_dir
    output: html or csv
    """
    try:
        c = load_config(config)
    except:
        exit()
    cpath = Path(config).with_suffix('.yaml')
    if not cpath.exists():
        print('no config file found')
        exit()
    cf = yaml.load(cpath.read_text())

    ct = CherryTree(cf['content_index'])

    cbn = cf['content_base_name']
    cfd = cf['content_file_dir']

    content_base_node = ct.find_node_by_name(cbn)

    if not content_base_node:
        print(f' {content_base_name} not in index')
        exit()

    for node in content_base_node.descendants:
        for item in node.text:
            print(item)





if __name__ == '__main__':
    plac.call(main)
