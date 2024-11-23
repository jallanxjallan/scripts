#!/home/jeremy/Python3.12Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import attr
from attr import define, field, fields
from pathlib import Path
import yaml
import atexit
import pyperclip
from oaiv2 import Instructor, Processor, DataStore, Writer, trap_input_error
from document import Document
from utility import rand_string, load_config, snake_case
from oaiv2.constants import *

import fire 

def store_init_data(self, prompt, metadata):
	r_prompt = self.redis_key(PROMPT, 0)
	r_prompt.set(prompt) 
	r_metadata = self.redis_key(METADATA, 0)
	r_metadata.hset(mapping=metadata)
	r_metadata.hset(NAMESPACE, self.namespace)
	self.store_process_keys(r_metadata, r_prompt) 

@define
class ContentGen(DataStore, Processor, Writer):
	"""Base class with the namespace attribute and post-init processing."""
	project: str = field(default='general')
	context: str = field(default='generic')
	namespace: str = field(init=False, default=None)
	process_index: object = field(init=False, default=None)
	instructions: object = field(init=False, default=None)
	job: str = field(init=False, default=None)
	

	def __attrs_post_init__(self):
		# Set namespace based on projet if available, or use a three letter random string
		
		self.namespace = f'{self.project}.{rand_string()}'
		self.process_index = self.redis_key(PROCESS_INDEX)
		self.instructions = Instructor.load('instructions.md')
		# set expire for all keys in namespace
		atexit.register(self.set_expiry) 

	@trap_input_error
	def document(self, filepath):
		doc = Document.read_file(filepath)
		metadata = doc.metadata
		metadata[SOURCE] = doc.filepath.stem
		store_init_data(self, doc.content, metadata)
		self.job = snake_case(doc.filepath.stem)
		return self 

	@trap_input_error
	def cliptext(self): 
		prompt = pyperclip.paste() 
		if len(prompt.strip()) < 25:
			raise ValueError(f'{prompt} too short')
		store_init_data(self, prompt, source=CLIPPING)
		self.job = CLIPPING
		return self 
	
	@trap_input_error 
	def audio(self, filepath):
		fp = Path(filepath) 
		self.job = fp.parts[-2].split(DELIMITER)[0] 
		store_init_data(self, str(fp), source=fp.parts[-2])
		return self


	def display(self, att):
		print(getattr(self, att))

# CLI entry point using Fire
if __name__ == "__main__":
	config = load_config()

	with open('config.yaml', 'r') as file:
		config =  yaml.safe_load(file)
		fields_to_input = {k:v for k,v in config.items() if k in fields(ContentGen)} 
		class_instance = ContentGen(**fields_to_input)
	fire.Fire(class_instance)


	# Create a dynamic subclass of BaseConfig with fields from the YAML data
	# DynamicClass = attr.make_class(
	# 	"DynamicClass",
	# 	{key: attr.field(default=value) for key, value in config.items()},
	# 	bases=(ContentGen, DataStore, Processor, Writer)
	# )
	
	# # Instantiate the class and expose its methods to Fire CLI
	# fire.Fire(DynamicClass)


