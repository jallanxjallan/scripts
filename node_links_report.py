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

def main(source_index, outputfile, anchor_base, link_base='Scenes'):
    ct = CherryTree(source_index)
    if anchor_base:
        anchor_base_node = ct.find_node_by_name(anchor_base)
    else:
        anchor_base_node = ct.root
    link_base_node = ct.find_node_by_name(link_base)


    anchors = [a for n in anchor_base_node.descendants for a in n.anchors]

    links = [l for n in link_base_node.descendants for l in n.links if l.node_anchor]

    with open(outputfile, 'w') as outfile:
        print(f'{anchor_base} anchors  not linked to {link_base}', file=outfile)
        for name in set((a.name for a in anchors)).difference(set((l.node_anchor for l in links))):
            anc = next((a for a in anchors if a.name == name), None)
            print(f'Node: {anc.node.name} - Anchor: {anc.name}', file=outfile)

    print('finished')


if __name__ == '__main__':
    plac.call(main)
