#!/home/jeremy/Python3.12Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2023 Jeremy Allan <jeremy@jeremyallan.com> 

from pathlib import Path
from  attr import define, field, Factory
from oaiv2 import NotePrompt, DocPrompt, ChatInstructions, Chat, OutputDoc, DataStore, DataLoader
from common import initialize_class, ContentGen, Processor, Writer, trap_input_error
import pyperclip
from utility import snake_case
import fire

@define
class StoryGen(ContentGen):
	profile: str # redis key of selected profile
	datastore: object = field(default=Factory(lambda self: DataStore(context=
	
	

	@trap_input_error
    def get_prompt(self, note_ref=None):
		self.prompt_key = self.datastore.store_data('prompt', NotePrompt(text=pyperclip.paste()))
		
        prompt = NotePrompt.load_ref(note_ref or pyperclip.paste())
        self.prompts = [t for t in chunk_text(str(prompt))] 
        self.outputfile = self.documentpath.joinpath(snake_case(prompt.node.name)).with_suffix('.md')
        self.metadata.update(title=prompt.node.name, identifier=int(prompt.node.unique_id))
        return self 

	

def init_class(**kwargs):
	return initialize_class(StoryGen, **kwargs)

if __name__ == "__main__":
	fire.Fire(init_class)

