#!/home/jeremy/Python3.12Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2023 Jeremy Allan <jeremy@jeremyallan.com> 

from attr import define, field
from oai import NotePrompt, ChatInstruction, OutputDoc, chat
from storage import CherryTree, open_node_ref
from utility import staging_file, snake_case
from pathlib import Path
from resource import DataSource
import zipfile
import subprocess
import fire

class ContentWriter():
    def __init__(self, note_file=None):
        self.ct = CherryTree(note_file)
        self.nodes = [] 

    def display_nodes(self):
        for node in self.nodes:
            print(node)
    
    def submit_content(self, zip_name):
        with zipfile.ZipFile(zip_name, 'w') as zip_file:
            for node in self.nodes:
                input_filepath = self.edit_path.joinpath(snake_case(node.name)).with_suffix('.md')
                outputfile = staging_file(suffix='docx') 
                outputfilename = input_filepath.with_suffix('.docx')
                # title = f'title=Working Title: {item.name_source}'
                command = ['pandoc', '-o', str(outputfile), str(input_filepath)]
                rs = subprocess.run(command, capture_output=True)
                zip_file.write(outputfile, outputfilename) 
    
    def write_content(self, instructions, prompt, overwrite=False, model=3):
        op = OutputDoc(folder=self.edit_path, 
                    docname=prompt.note.name, 
                    title=prompt.note.name, 
                    identifier=prompt.note.unique_id, 
                    overwrite=overwrite)
        rs = chat(instructions, prompt, model=model)
        print(op.write_results(rs)) 
    
    def node_ref(self, node_ref):
        node = open_node_ref(node_ref)
        self.nodes.append(node)
        return self

    def node_list(self, node_list):
        with Path(node_list).open() as fp:
            for line in fp.readlines():
                try:
                    self.nodes.append(open_node_ref(line))
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
    fire.Fire(ContentWriter)