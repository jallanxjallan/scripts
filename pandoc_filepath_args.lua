#!/usr/bin/lua 
local p = require("path") 

local output_directory
local output_extension

function make_output_filepath(input_filepath) 
  local output_filepath
  if arg[1] == nil then 
    output_filepath  = os.tmpname()..'.md' 
  else 
    output_directory = p.dirname(arg[1])
    output_extension = p.extname(arg[1])
 
    local input_filename =  p.basename(input_filepath):gsub(' ', '_'):lower()
    local input_extension = p.extname(input_filepath)
    local output_filename = input_filename:gsub(input_extension, output_extension)
    output_filepath = output_directory..'/'..output_filename 
  end
  return output_filepath
end

for input_filepath in io.lines() do 
  local output_filepath = make_output_filepath(input_filepath)
    print('--output='..output_filepath..' '..input_filepath)
end
  
