#!/home/jeremy/Python3.12Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2023 Jeremy Allan <jeremy@jeremyallan.com> 

from pathlib import Path
import re
import time
from document import Document
from utility import timestamp, snake_case
import fire 


# Compile the pattern outside the function
basename_pattern = re.compile(r"([A-Za-z_]+)_(\d+)\.txt")
trailing_id_pattern = re.compile(r'_\d+\.txt$')
ordered_list_pattern = re.compile(r"^\d+\.\s+.*")
document_title_pattern = re.compile(r'^(#{1,6})\s+(.*)')


def find_leaf_nodes(export_dir):
    # Read in all the filenames
    export_path = Path(export_dir)
    files = [str(fp) for fp in export_path.iterdir()]
    
    
    # Convert filenames to a set for quick lookup
    files_set = set(files)
    
    
    for file in files:
        # Skip root nodes (those without '--')
        if '--' not in file:
            continue
        
        # Remove the trailing ID with regex
        base_name = re.sub(trailing_id_pattern, '', file)  # Removes '_<ID>.txt' at the end
        # Generate the prefix that would indicate children nodes
        prefix = f"{base_name}--"
        
        # Assume this file is a leaf until we find a child
        is_leaf = True
        
        # Check if any other file starts with this base name + '--'
        for other_file in files_set:
            if other_file.startswith(prefix):
                is_leaf = False
                break
        
        # If no children were found, it's a leaf node
        if is_leaf:
            yield Path(file)
    
def export_leaf(filepath, story_path):
    path_parts = filepath.parts
    leaf_parts = path_parts[-1].split('--')

    basename, identifier = basename_pattern.findall(leaf_parts[-1])[0] 
    story_filepath = story_path.joinpath(snake_case(basename)).with_suffix('.md') 
    if story_filepath.exists():
        return 0
    
    numbered_list_items = []

    # Read the file and extract numbered list items
    with filepath.open("r") as file:
        first_line = file.readline().strip()
        if (m := document_title_pattern.match(first_line)):
            prefix, title = m.groups() 
        else:
            title = 'No title'
       
        for line in file:
            if ordered_list_pattern.match(line.strip()):
                numbered_list_items.append(line.strip())

    # Output the extracted list items
    if len(numbered_list_items) == 0:
        return 0 
    
   
   
    Document(content='\n\n'.join(numbered_list_items),
             metadata=dict(title=title, 
                           identifier=int(identifier), 
                           status='exported', 
                           created=timestamp(),
                           parents=leaf_parts[:-1])
             ).write_file(story_filepath)
    return 1

def main(export_dir, story_dir):
    exported_stories = 0
    for filepath in find_leaf_nodes(export_dir):
        exported_stories += export_leaf(filepath, Path(story_dir))
    print(f'{exported_stories} notes exported to {story_dir}')
       

if __name__ == '__main__':
    fire.Fire(main)

