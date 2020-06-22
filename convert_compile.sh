tmpdir=$(mktemp -d)
i=1000
while IFS= read rkey
do
  i=$((i+10))
  outputfile=$tmpdir/inter_$i.md
  defaults=$(redis-cli hget $rkey defaults)
  if [ $(redis-cli hexists $rkey filepath) ]
  then
    filepath=$(redis-cli hget $rkey filepath)
  else
    filepath=$(mktemp --tmpdir=$tmpdir)
    text=$(redis-cli hget $rkey text)
    echo $text > $filepath
  fi
  pandoc -o $outputfile $filepath
done


pandoc -o output/test_compile.docx $tmpdir/inter_*.md

rm -rf $tmpdir
