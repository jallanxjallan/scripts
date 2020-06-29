#!/home/jeremy/Python3.6Env/bin/python
# * coding: utf8 *
#
#  update_document_index.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import re
from pathlib import Path
import datetime
from uuid import uuid4
import attr
import fire

sys.path.append('/home/jeremy/Library')

from editing.document_index import DocumentIndex, load_document

class Updater():
    def __init__(self, index_file):
        try:
            self.di = DocumentIndex(index_file)
        except Exception as e:
            print(e)
            raise

    def add_from_filelist(self, filelist, target=None):
        fp = Path(filelist)
        added = False

        for filepath in [Path(f) for f in fp.read_text().split("\n")]:
            rs = self.di.insert_entry(filepath, target)
            if rs:
                added = True
                print(rs)
        if added:
            pass
            # self.di.sve_index()
        return True

    def add_from_filename(self, filepath, target=None):
        rs = self.di.insert_entry(filepath, target)
        if rs:
            print(rs)
          # self.di.save_index()

    def add_from_stream(self, target):
        added = False
        for filepath in sys.stdin.readlines():
            rs = self.di.insert_entry(filepath.strip(), target)
            if rs:
                added = True
                print(rs)
        if added:
            pass
            # self.di.save_index()
        return True

    def add_file_links(self, source_dir, target='existing'):
        added = False
        for filepath in [f for f in Path(source_dir).iterdir() if f.suffix == '.md']:
            document = load_document(filepath)
            if not document:
                continue
            if self.di.find_entry_by_identifier(document.identifier):
                continue
            node = self.di.find_entry_by_name(document.title)
            if not node:
                print('Cannot find node matching', document.title)
                continue
            rs = self.di.insert_document_link(node, document)
            if rs:
                added = True
                print(f'linked {node.name} to {filepath}')
        if added:
            self.di.save_index()
        return True

if __name__ == '__main__':
    fire.Fire(Updater)
