while IFS= read line; do
    pandoc -d $line
    echo $line
done
