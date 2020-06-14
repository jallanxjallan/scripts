#!/usr/bin/env bash
read rkey
defaults_files_key = $(redis-cli hget $rkey defaults_files)
echo "$defaults_files_key"
# for filename in $(redis-cli lpop $defaults_files_key); do
  # echo $filename
  # do
  #   defaults=$(redis-cli hget $rkey defaults)
  #   outfile=$(redis-cli hget $rkey outfile)
  #   sequence=$(redis-cli hget $rkey sequence)
  #   title=$(redis-cli hget $rkey title)
  #   input=$(redis-cli hget $rkey input)
  #   tmpfile=$(mktemp)
  #   echo "$input" > $tmpfile
  #   pandoc -d $defaults -o $outfile $tmpfile
  #   rm $tmpfile
# done
