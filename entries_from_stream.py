#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import fire
from pathlib import Path

sys.path.append('/home/jeremy/Library')

from editing.document_index import DocumentIndex


def add_from_stream(index_file):
    idx = DocumentIndex(index_file)
    for filepath in sys.stdin.readlines():
        fp = Path(filepath.strip())
        rs = idx.add_document(fp)
        print(rs)
    # idx.save_index()

if __name__ == '__main__':
    fire.Fire(add_from_stream)
