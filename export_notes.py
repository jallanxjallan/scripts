#!/home/jeremy/Python3.12Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2023 Jeremy Allan <jeremy@jeremyallan.com> 

from pathlib import Path
from collections import defaultdict
import re
import redis
from document import Document
from utility import timestamp, snake_case
import fire 

r = redis.Redis()

# Compile the pattern outside the function
basename_pattern = re.compile(r"([A-Za-z_]+)_(\d+)\.txt")
ordered_list_pattern = re.compile(r"^\d+\.\s+(.*)")
node_heading_pattern = re.compile(r'^(#{1,6})\s+(.*)') 

# Recursive function to find the parent chain for each item
def find_parents(hierarchy, item_id):
	# Base case: if the item has no parent, return an empty list (it's a root)
	item = hierarchy[item_id]
	if item['parent'] is None:
		return []
	
	# Recursive case: find the parents of the item's parent, then add this parent
	parent_chain = find_parents(hierarchy, item['parent'])
	parent_chain.append(item['parent'])  # Append the parent's ID to the chain
	return parent_chain

def load_notes_output_file(file_path):
	hierarchy = []  # This will store the final list of headings with hierarchy info
	stack = []      # Stack to keep track of the current hierarchy levels (parent-child relationship)
	
	with file_path.open() as file:
		for line in file:
			line = line.strip()
			
			# Identify headings by the number of leading '#' characters
			if line.startswith('#'):
				level = line.count('#')  # The level is determined by the number of '#'s
				heading = line[level:].strip()  # The text of the heading after the '#' symbols
				
				# Pop stack until it matches the level to maintain correct hierarchy
				while stack and stack[-1]["level"] >= level:
					stack.pop()
				
				# Determine the parent based on the last item in the stack
				parent = stack[-1] if stack else None
				parent_id = parent['id'] if parent else None  # Parent ID, if exists
				
				# Create a unique ID for each heading based on its index in the hierarchy list
				heading_id = len(hierarchy)
				
				# Store the heading in the hierarchy with level, text, and parent info
				heading_info = {
					"id": heading_id,
					"level": level,
					"heading": heading,
					"parent": parent_id,
					"texts": []
				}
				hierarchy.append(heading_info)
				
				# Add this heading to the stack as the latest item in the hierarchy
				stack.append(heading_info) 
			elif (m := ordered_list_pattern.match(line)):
				stack[-1]['texts'].append(m.group(1)) 

	parent_chains = {
		item['id']: find_parents(hierarchy, item['id'])
		for item in hierarchy if item['parent'] is not None
	}
	
	return hierarchy, parent_chains

def upload_instructions(filepath):
	if not (fp := Path(filepath)).exists():
		raise FileNotFoundError
	
	hierarchy, parent_chains = load_notes_output_file(fp)
	# Generate a dictionary of parent chains for all items that are not roots

	for item in [i for i in hierarchy if i['id'] not in [p for v in parent_chains.values() for p in v]]:
		parents = [hierarchy[p] for p in parent_chains[item['id']]]
		key = ['instructions']
		key.extend([snake_case(p['heading']) for p in parents])
		key.append(snake_case(item['heading']))
		instructions = [t for p in parents for t in p['texts']]
		instructions.extend(item['texts'])
		inst_key = ':'.join(key)
		inst_string = '\n'.join([f'{i+1}. {t}' for i,t in enumerate(instructions)])
		r.set(inst_key, inst_string) 

def make_stories(note_path, story_path):
	if not (fp := Path(note_path)).exists():
		raise FileNotFoundError 
	
	sp = Path(story_path)
	
	hierarchy, parent_chains = load_notes_output_file(fp) 
	for item in [i for i in hierarchy if i['id'] not in [p for v in parent_chains.values() for p in v]]:
		story_filepath = sp.joinpath(snake_case(item['heading'])).with_suffix('.md') 
		if story_filepath.exists():
			return 0
		parents = [hierarchy[p]['heading'] for p in parent_chains[item['id']]] 

		Document(content=item['texts'],
				metadata=dict(title=item['heading'], 
							status='exported', 
							created=timestamp(),
							parents=parents)
				).write_file(story_filepath)

if __name__ == '__main__':
	fire.Fire({'instructions':upload_instructions, 'stories':make_stories})

