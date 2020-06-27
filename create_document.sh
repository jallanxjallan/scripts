
filepath=$1

if test -f $filepath; then
  echo "$filepath already exists"
else
  title=$(basename $filepath | sed s/\.md//g | sed 's/_/ /g' | sed -e "s/\b\(.\)/\u\1/g")
  pandoc -d create_document \
  -M title=title \
  -f markdown \
  -o $filepath
  echo file://$(pwd)/$filepath
fi
