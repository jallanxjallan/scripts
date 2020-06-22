tmpdir=$(mktemp -d)

input_file=$1
target_dir=$2
source=$3


pandoc \
--lua-filter=comment_to_inline.lua \
--lua-filter=split_document_on_header.lua \
--track-changes=all \
-M target_dir=$tmpdir \
-M source=$source \
"$input_file"

for filepath in $tmpdir/*.json; do
  filename=$(basename $filepath .json)
  outputfile=$target_dir/$filename.md

  pandoc \
  -d create_document \
  -s \
  --lua-filter=title_from_header.lua \
  -o $outputfile \
  $filepath
done
rm -rf $tmpdir
