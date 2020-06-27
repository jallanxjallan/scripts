#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import re
import fire
from pathlib import Path

sys.path.append('/home/jeremy/Library')


from document.md_document import read_file
from editing.document_index import DocumentIndex


def add_file_links(index_file, source_dir):
    idx = DocumentIndex(index_file)
    for filepath in Path(source_dir).iterdir():
        rs = idx.add_file_link(str(filepath))
        print(rs)
    idx.save_index()

if __name__ == '__main__':
    fire.Fire(add_file_links)
