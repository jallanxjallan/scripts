#!/home/jeremy/Python3.12Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import attr
import yaml
from oaiv2 import ContentGen, Processor, DataStore, Writer
import fire


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
