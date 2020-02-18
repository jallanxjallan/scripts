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

def main(config_path):
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

    cpath = Path(config_path)
    if not cpath.exists():
        print('no config found')
        exit()
    config = yaml.load(cpath.read_text())

    ct = CherryTree(config['source_index'])

    link_target_node = ct.find_node_by_name(config['target_name'])
    if not link_target_node:
        raise f'target node {target_name} not found'

    anchor_links = [l.node_anchor for n in link_target_node.descendants for l in n.links if l.node_anchor]

    unlinked_anchors = [(n.name, a.name) \
                        for c in category_nodes(config['categories']) \
                        for n in c.descendants \
                        for a in n.anchors \
                        if not a.name in anchor_links]

    df = pd.DataFrame(unlinked_anchors, columns=['Node', 'Anchor'])

    convert_text(df.sort_values('Node').to_html(), config['node_report_file'])
    print('finished')


if __name__ == '__main__':
    plac.call(main)
