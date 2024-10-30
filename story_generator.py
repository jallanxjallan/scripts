#!/home/jeremy/Python3.12Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2023 Jeremy Allan <jeremy@jeremyallan.com> 

from pathlib import Path
from  attr import define, field, Factory
from oaiv2 import NotePrompt, DocPrompt, ChatInstructions, Chat, OutputDoc, DataStore, DataLoader
from common import initialize_class, Reader, Processor, Writer
import fire

@define
class StoryGen(DataLoader):
	project: str = field()
	storypath: Path = field(default='stories', converter=Path)
	instructions: object = field(default=Factory(lambda self: ChatInstructions.load_instructions(self.project), takes_self=True))
	datastore: object = field(default=Factory(lambda self: DataStore.load_data(self.project), takes_self=True))

	

def init_class(**kwargs):
	return initialize_class(StoryGen, **kwargs)

if __name__ == "__main__":
	fire.Fire(init_class)

