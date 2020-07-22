tmpdir=$(mktemp -d)

while IFS= read fullpath; do
  filename=$(basename -- "$fullfile")
  stem="${filename%.*}"
  outputfile=$tmpdir/$stem.md
  pandoc -o $outputfile $fullpath
  echo $outputfile
done
echo $tmpdir
