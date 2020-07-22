
read -p 'Title: ' title
read -p 'Location: ' location
read -p 'Date: ' date

filename=$(echo $title | sed 's/ /_/g' | sed -e 's/\(.*\)/\L\1/')
filepath=new_scenes/$filename".md"

if test -f $filepath; then
  echo "$filepath already exists"
else
  pandoc -d create_scene \
  -M title="$title" \
  -M location="$location" \
  -M date="$date" \
  -f markdown \
  -o $filepath
  echo file://$(pwd)/$filepath
fi
