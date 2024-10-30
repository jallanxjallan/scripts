#!/home/jeremy/Python3.12Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import os
import sys
import importlib
from attrs import define, field
from script_lib import Analyser, initialize_class
from pathlib import Path
from storage import CherryTree
import fire


@define
class ContentAnalyse(Analyser):
    base_dir = field(converter=Path)
    index_file = field(default='content_index.md')
    doc_dir= field(default='stories', converter=Path)
    edit_path = field(default='edits', converter=Path)
    notes_file = field(default='story_notes', converter=CherryTree)
   
    
def init_class(**kwargs):
    return initialize_class(ContentAnalyse, **kwargs)

if __name__ == "__main__":
    fire.Fire(init_class)