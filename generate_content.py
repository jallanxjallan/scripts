#!/home/jeremy/Python3.12Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import attr
from attr import define, field
from pathlib import Path
import yaml
import atexit
import pyperclip
from oaiv2 import Processor, DataStore, Writer, trap_input_error
from document import Document
from utility import rand_string

import fire

@define
class ContentGen():
	"""Base class with the namespace attribute and post-init processing."""
	prompt: str = field(init=False, default=None)
	namespace: str = field(init=False, default=None)
	counter: str = field(init=False, default=None)
	process_index: object = field(init=False, default=None)
	job: str = field(init=False, default=None)
	audiofile: Path = field(init=False, default=None)

	def __attrs_post_init__(self):
		# Set namespace based on context if available, or use "general"
		context = getattr(self, 'context', 'general')
		self.namespace = f"{context}.{rand_string()}"
		self.counter = self.redis_key('counter')
		self.counter.set(0)
		self.process_index = self.redis_key('process', 'index')
		# set expire for all keys in namespace
		atexit.register(self.set_expiry) 

	@trap_input_error
	def document(self, filepath):
		doc = Document.read_file(filepath)
		self.prompt = doc.content
		self.redis_key('metadata').hset(mapping=doc.metadata)
		inputfile = doc.metadata.get('inputfile', None)
		self.job = Path(inputfile).stem if inputfile else doc.filepath.stem
		return self 

	@trap_input_error
	def cliptext(self): 
		self.prompt = pyperclip.paste() 
		if len(self.prompt) < 25:
			raise ValueError(f'{self.prompt} too short')
		self.redis_key('source').set('clipping')
		self.job = 'clipping'
		return self 
	
	@trap_input_error 
	def audio(self, filepath):
		fp = Path(filepath) 
		source = fp.parts[-2]
		self.audiofile = fp
		self.job = fp.parts[-2].split('qq')[0] 
		self.redis_key('metadata').hset(
			mapping=dict(
				source=source,
				chunk=filepath))
		return self


# CLI entry point using Fire
if __name__ == "__main__":
	
	"""Create a dynamic subclass of BaseConfig based on key-value pairs from a YAML file."""
	with open('config.yaml', 'r') as file:
		config =  yaml.safe_load(file)


	# Create a dynamic subclass of BaseConfig with fields from the YAML data
	DynamicClass = attr.make_class(
		"DynamicClass",
		{key: attr.field(default=value) for key, value in config.items()},
		bases=(ContentGen, DataStore, Processor, Writer)
	)
	
	# Instantiate the class and expose its methods to Fire CLI
	fire.Fire(DynamicClass)


