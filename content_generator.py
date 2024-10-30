#!/home/jeremy/Python3.12Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2023 Jeremy Allan <jeremy@jeremyallan.com> 

from pathlib import Path
from  attr import define, field, Factory
from script_lib import Reader, Processor, Writer, Instructor, initialize_class
from utility import rand_string
import fire

@define
class ContentGen(Reader, Processor, Writer):
	project: str = field(default=Factory(lambda: rand_string(8)))
	job: str = field(default=Factory(lambda: rand_string(8)))
	editpath: Path = field(default='edits', converter=Path)
	sourcepath: Path = field(default='.', converter=Path)
	documentpath: Path = field(default='stories', converter=Path)
	instructions: object = field(default=Factory(lambda self: Instructor.load_instructions(self.project), takes_self=True))   
	metadata: dict = field(default={}) 

def init_class(**kwargs):
	return initialize_class(ContentGen, **kwargs)

if __name__ == "__main__":
	fire.Fire(init_class)

