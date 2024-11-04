#!/home/jeremy/Python3.12Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
from pathlib import Path
import attr
from attr import define, field
import yaml
from oaiv2 import Processor, DataStore, Writer
from utility import rand_string
from document import Document
import atexit
import fileinput
import fire 


def load_input_arg():
	for line in fileinput.input():
		filename = line.strip()  # Remove any extra whitespace
		# doc = Document.read_file(filename) 
		break
	return filename
	# print(arg)
	# if arg.startswith('---'):
	# 	return Document.read_text(arg) 
	# elif (fp := Path(arg)).exists():
	# 	return 
	# else:
	# 	raise ValueError(f'{arg} not a valid input')


@define
class ContentGen():
	"""Base class with the namespace attribute and post-init processing."""
	prompt: str = field(init=False, default=None)
	namespace: str = field(init=False, default=None)
	counter: str = field(init=False, default=None)
	process_index: object = field(init=False, default=None)

	def __attrs_post_init__(self):
		# Set namespace based on context if available, or use "general"
		context = getattr(self, 'context', 'general')
		self.namespace = f"{context}_{rand_string()}"
		self.counter = self.redis_key('counter')
		self.counter.set(0)
		self.process_index = self.redis_key('process', 'index')
		# set expire for all keys in namespace
		atexit.register(self.set_expiry) 

	def filepath(self, filepath):
		doc = Document.read_file(filepath)
		self.prompt = doc.content
		self.redis_key('metadata').hset(mapping=doc.metadata)
		self.redis_key('source').set(str(doc.filepath))
		return self
	
	def display(self):
		"""Display current configuration including namespace."""
		print(self.namespace, self.prompt.title)
	

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
