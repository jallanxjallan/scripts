read -p 'Title: ' title
if [ -n ${fdr} ]; then
  target_folder=$fdr
else
  read -p 'Folder: ' target_folder
fi

if [ -n ${dft} ]; then
  defaults=$dft
else
  read -p 'Defaults: ' defaults
fi

filename=$(echo $title | sed 's/ /_/g' | sed -e 's/\(.*\)/\L\1/')
filepath=$target_folder/$filename".md"

if test -f $filepath; then
  echo "$filepath already exists"
  exit
fi
read -p "Create $filepath with $defaults? y/n" proceed
# if [$proceed -eq "y"]; then
#   pandoc -d $dft \
#   -M title="$title" \
#   -f markdown \
#   -o $filepath
#   echo file://$(pwd)/$filepath
# fi
