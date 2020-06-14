#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import fire
from pathlib import Path
import spacy
import pandas as pd

sys.path.append('/home/jeremy/Library')

from storage.cherrytree_xml import CherryTree
from document.read_document import read_document

nlp = spacy.load('en_core_web_sm')

def extract_named_entities(text_index, target_node):
    ct = CherryTree(text_index)
    if target_node:
        node = ct.find(target_node)
    else:
        node = ct.root

    documents = [(read_document(n.textfile), n) for n in node.subnodes()]

    docs = nlp.pipe([(t.content, t) for t in documents], as_tuples=True)

    for (node, ent) in [(d[1], e) for for d in docs for e in d[0].ents]:
        yield (node, ent)


if __name__ == '__main__':
    return fire.Fire(extract_named_entities)
