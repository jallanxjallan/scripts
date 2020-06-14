read tmpdir
for filename in /Data/$tmpdir/*.yaml;
do
  echo $filename
  # pandoc -d $filename
done

# rm -rf $tmpdir
