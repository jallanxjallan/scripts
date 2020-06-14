#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import fire
from pathlib import Path
import sys
import re
sys.path.append('/home/jeremy/Library')

from document.document_index import DocumentIndex
from document.md_document import read_text


def create_document(filepath):
    base_path = Path.cwd()
    filepath = Path(filepath)
    if filepath.exists():
        print(filepath, 'already exists')
        return False
    document = read_text(sys.stdin.read())
    try:
        identifier = document.identifier
    except AttributeError:
        print ('Document has no identifier')
        return False
    title = re.sub('\_|\-', ' ', filepath.stem).title()
    document.metadata['title'] = title
    idx = DocumentIndex()
    try:
        idx.add_document(document, str(filepath))
    except Exception as e:
        print(e)
        return False
    idx.ct.save()
    fullpath = base_path.joinpath(filepath)
    document.write_document(fullpath)
    print(f'file://{str(fullpath)}')

if __name__ == '__main__':
    fire.Fire(create_document)
