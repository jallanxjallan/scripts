tmpdir=$(mktemp -d)

input_file=$1
target_dir=$2
source_prefix=$3
filelist=$tmpdir/filelist.txt

pandoc \
--lua-filter=split_document_on_header.lua \
-M target=$tmpdir \
-M source=$source_prefix \
$1

for filepath in $tmpdir/*.json; do
  filename=$(basename $filepath .json)
  outputfile=$target_dir/$filename.md
  echo $outputfile
  pandoc \
  -d create_document \
  -s \
  --lua-filter=title_from_header.lua \
  -o $outputfile \
  $filepath
done | update_document_index.py add_from_stream

rm -rf $tmpdir
