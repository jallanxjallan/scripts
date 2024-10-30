#!/home/jeremy/Python3.12Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2023 Jeremy Allan <jeremy@jeremyallan.com> 

from oai import NotePrompt, ChatInstructions, OutputDoc, chat
from storage import CherryTree, open_node_ref
from pathlib import Path
import fire

class Submitter():
    def __init__(self, note_file=None):
        self.ct = CherryTree(note_file)
        self.nodes = [] 
    
    def node_ref(self, node_ref):
        node = open_node_ref(node_ref)
        self.nodes.append(node)
        return self

    def node_list(self, node_list, note_file=None):
        with Path(node_list).open() as fp:
            for line in fp.readlines:
                try:
                    self.nodes.append(open_node_ref(line, note_file=note_file))
                except ValueError:
                    print(f'Invalid node ref {line}')
                    continue
        return self
    
    def all_nodes(self, note_file, base_node):
        ct = CherryTree(note_file) 
        base = ct.find_node_by_name(base_node)
        self.nodes =  base.children()
        return self
        
if __name__ == "__main__":
    fire.Fire(Submitter)