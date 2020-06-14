tmpdir=$(mktemp -d)
read rkey
defaults_files_key = $(redis-cli hget $rkey defaults_files)
echo "$defaults_files_key"
# for filename in $(redis-cli lpop $defaults_files_key); do
  # echo $filename
  # do
  cmd = 'pandoc'
  cmd = cmd + ' -d $defaults'
  for key in redis-cli get input file
    value = redis-cli hget key
    cmd = cmd + ' -M $key=$value'
  cmd = cmd + ' -o $outputfile $inputfile'

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

no=100
while IFS= read line; do
    pandoc -d inter_compile -o $tmpdir/$no.md $line
    no=$((no+10))
done
pandoc -d output_compile -o $1 $tmpdir/*.md
rm -rf $tmpdir
