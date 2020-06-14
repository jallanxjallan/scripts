#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  update_document_index.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import re
from pathlib import Path
import datetime
import attr
import fire
import inflect

sys.path.append('/home/jeremy/Library')

from storage.cherrytree_xml import CherryTree
from document.md_document import read_file

@attr.s
class Document():
    index = attr.ib()
    document = attr.ib()
    filepath = attr.ib()

class DocumentIndex():
    def __init__(self, index_file='document_index.ctd'):
        try:
            self.ct = CherryTree(index_file)
        except Exception as e:
            print(e)
            raise

    def documents(self, base=None):
        for node in self.ct.nodes(base):
            filelink = next((l for l in node.links if l.type == 'file'), None)
            if not filelink:
                continue
            document = self.load_document(filelink.href)
            if not document:
                continue
            yield Document(node, document, filelink)

    # def store_document_data(self, node, data):
    #     if not type(data) is str:
    #         content = dump_yaml(data)
    #     else:
    #         content = data
    #
    #     codebox = next((c for c in node.codeboxes), None)
    #     if codebox:
    #         codebox.content = content
    #     else:
    #         node.insert_codebox(content=dump_yaml(content), language='yaml')


    def add_document(self, filepath):
        try:
            document = read_file(filepath)
        except FileNotFoundError:
            print(filepath, 'not found')
            return False

        if self.ct.find_node_by_text(document.identifier):
            print(filepath, 'already indexed')
            return True
        new_items = self.ct.find_node_by_name('New Items') \
            or self.ct.insert_node('New Items')
        node = self.ct.insert_node(document.title, target=new_items)
        anchor = node.insert_anchor(name=document.identifier)
        link = node.insert_link(href=filepath, text="File", target=anchor)
        new_line = node.insert_text('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        return filepath

    def add_from_filelist(self, filelist):
        fp = Path(filelist)
        if not fp.exists():
            return fp, 'Not Found'
        added = []
        for filepath in [Path(f) for f in fp.read_text().split("\n")]:
            added.append(self.add_document(filepath))
        self.save_index(added)

    def save_index(self, added):
        indexed_files = [f for f in added if not f is None]
        if len(indexed_files) == 0:
            return 'No Documents Indexed'
        self.ct.save()
        for filename in indexed_files:
            print(f'stored {str(filename)} to self.document_index')
        return True

    def add_from_filename(self, filepath):
        rs = self.add_document(filepath)
        if rs:
            self.save_index([rs])
        return True

    def add_from_stream(self):
        added = []
        for filepath in [s.strip() for s in sys.stdin.readlines()]:
            added.append(self.add_document(filepath))
        self.save_index(added)
        return True


if __name__ == '__main__':
    fire.Fire(DocumentIndex)

# @property
#     def text_filepath(self):
#         filepath = None
#         codebox = self.codebox
#         if codebox and hasattr(codebox, 'filepath'):
#             filepath = codebox.filepath
#         else:
#             filepath = next((l.filepath for l in self.links if l.filepath), None)
#         return filepath
#
# def __attrs_post_init__(self):
#         yaml = YAML()
#         if len(self.data) > 0:
#             if type(self.data) is str:
#                 self.data = yaml.load(self.data)
#         else:
#             self.data = yaml.load(self.codebox.text)
#
#     def __str__(self):
#
#         stream = StringIO()
#         yaml.dump(self.codebox.text, stream)
#         stream.seek(0)
#         return stream.read()
#
#     def __getattr__(self, att):
#         return self.codebox.get(att, None)
# yaml=YAML()
# p = inflect.engine()
# # nlp = spacy.load('en_core_web_sm')
#



    # ct = CherryTree(index_file)


    #     print('===========')
        # node = ct.find_node_by_text(document.identifier)
        # file_link = Link(None, document.filepath, 'Text')
        # metadata = CodeBox(None, document.metadata)
        # if node:
        #     node
        #
        #     node = Node(None, links=file_link, codeboxes=metadata)
        # try:
        #     node_data = YAMLDocument(next(c.content for c in node.codeboxes))
        # except Exception as e:
        #     print(e)
        #     continue












        # node = ct.create_node(title.title())
        # node.make_file_link(filepath, 'Text')
        # node.update_insert_codebox(metadata)
        # shutil.move(str(source_filepath), str(target_filepath))
        # ct.save()



# @property
#     def text_filepath(self):
#         filepath = None
#         codebox = self.codebox
#         if codebox and hasattr(codebox, 'filepath'):
#             filepath = codebox.filepath
#         else:
#             filepath = next((l.filepath for l in self.links if l.filepath), None)
#         return filepath
#
# def __attrs_post_init__(self):
#         yaml = YAML()
#         if len(self.data) > 0:
#             if type(self.data) is str:
#                 self.data = yaml.load(self.data)
#         else:
#             self.data = yaml.load(self.codebox.text)
#
#     def __str__(self):
#
#         stream = StringIO()
#         yaml.dump(self.codebox.text, stream)
#         stream.seek(0)
#         return stream.read()
#
#     def __getattr__(self, att):
#         return self.codebox.get(att, None)
# yaml=YAML()
# p = inflect.engine()
# # nlp = spacy.load('en_core_web_sm')
#


# def update_document_index(index_file = 'document_index.ctd', include_content=False):
#     index_path = Path(index_file)
#     if not index_path.exists():
#         print(f'{Index_file} not found')
#         return False
#     elif not index_path.suffix == '.ctd':
#         print(f'{Index_file} not xml format')
#         return False
#
#
#     # ct = CherryTree(index_file)
#
#     for text in sys.stdin.readlines():
#         print(text)
#         print('===========')
        # node = ct.find_node_by_text(document.identifier)
        # file_link = Link(None, document.filepath, 'Text')
        # metadata = CodeBox(None, document.metadata)
        # if node:
        #     node
        #
        #     node = Node(None, links=file_link, codeboxes=metadata)
        # try:
        #     node_data = YAMLDocument(next(c.content for c in node.codeboxes))
        # except Exception as e:
        #     print(e)
        #     continue












        # node = ct.create_node(title.title())
        # node.make_file_link(filepath, 'Text')
        # node.update_insert_codebox(metadata)
        # shutil.move(str(source_filepath), str(target_filepath))
        # ct.save()
