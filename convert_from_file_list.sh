tmpdir=$(mktemp -d)
no=1
while IFS= read line; do
    pandoc -f markdown -t markdown -o $tmpdir/$no.md $line
    no=$((no+1))
done
echo $tmpdir
