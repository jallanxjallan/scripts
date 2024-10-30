#!/home/jeremy/Python3.12Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2023 Jeremy Allan <jeremy@jeremyallan.com> 

import os
import sys
import importlib
from attrs import define, field, Factory
from script_lib import Reader, initialize_class
from pathlib import Path
from document import Document
import fire

@define
class Placeholder(Reader):
	filepath = field(converter=Path)
	content = field()
	metadata = field(default={})
	project  = field(default=None)
	job = field(default=Factory(lambda self: self.filpath.stem, takes_self=True))
	doc_dir = field(default='stories', converter=Path)
	edit_path = field(default='edits', converter=Path)
	prompts = field(default=Factory(lambda self: self.content, takes_self=True))
	outputfile = field(init=False)
     
	def make_placeholder(self):
          note = self.note()
          metadata=note.metadata
          metadata['status'] = 'placeholder'
          return Document(content='No Text', metadata=metadata, filepath=note.outputfile).write_file()

def init_class(**kwargs):
    return initialize_class(Placeholder, **kwargs)

if __name__ == "__main__":
    inst = fire.Fire(init_class)
    inst.make_placeholder()