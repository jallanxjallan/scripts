no_docs=0
for filepath in $2/*.md; do
  echo $filepath
  uuid=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)
  document_key=$1:document:$uuid
  pandoc -t markdown \
  -M document_key=$document_key \
  -F store_metadata.py \
  -F store_comments.py \
  $filepath > /dev/null
  no_docs=$((no_docs+1))
done
echo "Indexed $no_docs documents in $2"
