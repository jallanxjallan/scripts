b#!/bin/bash
if [ "$1" == "-h" ]; then
  echo "Usage: defaults target-dir file-extention"
  exit 0
fi
while IFS= read srcfile
do
    filename=$(basename "$srcfile")
    dstfile="${filename%.*}"

    source=$(echo "$filename" | sed -e 's/[0-9]//g' -e 's/\.[a-zA-Z]*//g')
    sequence=$(echo "$filename" | sed -e 's/[a-zA-Z]//g' -e 's/\.//g')
    pandoc \
    -d $1 \
    -o $2/$dstfile.$3 \
    -M source=$source \
    -M sequence=$sequence \
    $srcfile
done
