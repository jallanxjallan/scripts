#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import re
import fire
from pathlib import Path

sys.path.append('/home/jeremy/Library')

from document.document_index import DocumentIndex




def store_document(filepath, input_file=None, index_file=None):
    base_path = Path.cwd()
    filepath = Path(filepath)
    if filepath.exists():
        print(filepath, 'already exists')
        return False
    inx = DocumentIndex(index_file)
    if input_file:
        inx.add_from_file(input_file)
    else:
        inx.add_from_stream()

        def add_from_file(self, filepath):
            try:
                document = self.load_document(filepath)
            except FileNotFoundError:
                print(filepath, 'not found')
                return False
            if self.add_document(document, filepath):
                self.ct.save()
                print(f'indexed {filepath}')
                return True

        def add_from_stream(self):
            added = 0
            for filepath in sys.stdin.readlines():
                echo "Test Title#This is  test#1" | cut -d# -f2
                try:
                    document = self.load_document(filepath.strip('\n'))
                except Exception as e:
                    print(e)
                    continue
                if self.add_document(document, filepath):
                    added += 1
            if added > 0:
                self.ct.save()
                print(f'indexed {str(added)} documents')
            return True





    write_text(sys.stdin.read())






    print(f'file://{Path.cwd()}/{filepath}')


if __name__ == '__main__':
    fire.Fire()
