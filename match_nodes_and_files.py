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

def main(config, output='csv'):
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

    file_links = set([l.filepath.stem \
                    for n in content_base_node.descendants \
                    for l in n.links \
                    if l.filepath
                    if cfd in str(l.filepath)
                    ])

    file_paths = set([f.stem \
        for f in Path(cfd).iterdir() \
        if f.suffix == '.md'])

    unmatched = [(f, None) for f in file_paths.difference(file_links)]
    unmatched.extend([(None, l) for l in file_links.difference(file_paths)])


    df = pd.DataFrame(unmatched, columns=['File', 'Link']).drop_duplicates().sort_values(['Link', 'File'])


    if output == 'csv':
        print(df.to_csv(sep=' ', index=False, header=False))

    elif output == 'html':
        print(df.to_html())
    else:
        print(f'unknown format {output}')


if __name__ == '__main__':
    plac.call(main)
