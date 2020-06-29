
read -p 'Title: ' title
read -p 'Folder ' doc_dir

filename=$(echo $title | sed 's/ /_/g' | sed -e 's/\(.*\)/\L\1/')
filepath=$doc_dir/$filename".md"

if test -f $filepath; then
  echo "$filepath already exists"
else
  pandoc -d create_document \
  -M title="$title" \
  -f markdown \
  -o $filepath
  echo file://$(pwd)/$filepath
fi
