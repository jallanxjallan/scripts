
text=$(pandoc -d import_document "$1")

redis_key=$(openssl rand -base64 12)

redis-cli hset $redis_key text "$text" > /dev/null

redis-cli hset $redis_key source "$1" > /dev/null

redis-cli expire $redis_key 100 > /dev/null

echo "$redis_key"


