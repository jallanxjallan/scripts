#!/home/jeremy/Python3.12Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2023 Jeremy Allan <jeremy@jeremyallan.com> 


from  attr import define, field
from oaiv2 import TextPrompt, ChatData
from common import ContentGen, Processor, trap_input_error, trap_output_error
from utility import rand_string
import pyperclip
import fire


def store_initial_prompt(func):
	@functools.wraps(wrapper)
	def wrapper(self, ):
		if not self.datastore:
			self.datastore = DataStore(context=self.content, item=self.item) 
		self.datastore.store_data

def get_args(func):
	@functools.wraps(wrapper)
	def wrapper(self, *kwargs):
		for 


@define
class ClipGen(ContentGen, Processor):
	context: str = field(default='clipping')
	item: str = field(default=rand_string())

	@store_data
	@trap_input_error 
	@get_args
	def cliptext(self, **kwargs):
		self.initial_prompt_key = self.datastore.store_initial_prompt(TextPrompt(text=pyperclip.paste()))
		return self 
	
	@trap_output_error 
	def clip(self):
		results = ChatData.from_dict(self.datastore.fetch_final_results())
		pyperclip.copy(results.content) 
		return 'chat results copied to clipboard'

if __name__ == "__main__":
	clipper = fire.Fire(ClipGen)
	clipper.cliptext()


