# tmpdir=$(mktemp -d)
tmpdir=interfiles
i=1000
while IFS= read rkey
do
  echo $rkey
  echo $(redis-cli hgetall $rkey)
  i=$(($i+10))
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
  echo pandoc --defaults=$defaults --output=$outputfile $filepath
done


# pandoc --output=$2 $tmpdir/inter_*.md

# rm -rf $tmpdir
