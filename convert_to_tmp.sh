tmpdir=$(mktemp -d)
no=100
while IFS= read line; do
    pandoc -d $1 -o $tmpdir/$no.md $line
    no=$((no+10))
done
echo $tmpdir
