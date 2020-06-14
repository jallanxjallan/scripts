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
from utility.helpers import snake_case

def main(config, category, output='html'):
    """Match anchors to targets in content branch of index
    config fields: content_index, content_base_name,
    output: html or csv
    """
    def category_nodes(names):
        for name in names:
            node = ct.find_node_by_name(name)
            if node:
                yield node
            else:
                raise f'category {name} not found'

    def make_output_item(name):
        anc = next((a for a in anchors if a.name == name), None)
        if anc:
            return (anc.node.name, anc.name)
        return None

    def find_unlinked_anchors(anchors):
        for node in set((a.name for a in anchors)).difference(set((l.node_anchor for l in links))):
            yield node

    cpath = Path(config).with_suffix('.yaml')
    if not cpath.exists():
        print('no config file found')
        exit()
    cf = yaml.load(cpath.read_text())

    ct = CherryTree(config['content_index'])

    content_base_node = ct.find_node_by_name(config['content_base_name'])
    if not content_base_node:
        raise f'base node {config['content_base_name']} not found'

    anchor_links = [l.node_anchor for n in link_target_node.descendants for l in n.links if l.node_anchor]

    unlinked_anchors = [(c.name, n.name, a.name) \
                        for c in category_nodes(config['categories']) \
                        for n in c.descendants \
                        for a in n.anchors \
                        if not a.name in anchor_links]

    df = pd.DataFrame(unlinked_anchors, columns=['Category', 'Node', 'Anchor'])

    report_path = Path(config['report_folder'])

    for category in df.Category.unique():
        convert_text(df[df.Category == category].sort_values('Node').to_html(),
                        report_path.joinpath(f'{snake_case(category)}_unlinked_anchors').with_suffix('.html'))
    print('finished')


if __name__ == '__main__':
    plac.call(main)
