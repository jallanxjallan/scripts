#!/home/jeremy/Python3.12Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2023 Jeremy Allan <jeremy@jeremyallan.com>  
import yaml
import redis
import fire

def upload_to_redis(yaml_file: str, namespace: str, redis_host='localhost', redis_port=6379):
    """
    Parse a YAML file and upload the content to Redis with the given namespace.
    
    Args:
    - yaml_file (str): Path to the YAML file to be parsed.
    - namespace (str): Namespace to prepend to Redis keys.
    - redis_host (str): Redis host (default 'localhost').
    - redis_port (int): Redis port (default 6379).
    """
    # Connect to Redis
    r = redis.Redis(host=redis_host, port=redis_port)
    
    # Load YAML file
    with open(yaml_file, 'r') as file:
        yaml_data = yaml.safe_load(file)
    
    # Iterate over the YAML data and upload to Redis
    for key, value in yaml_data.items():
        # Full Redis key with namespace
        redis_key = f"{namespace}:{key}"
        
        if isinstance(value, str):
            # If the value is a string, use SET
            r.set(redis_key, value)
            print(f"Set string key: {redis_key} -> {value}")
        
        elif isinstance(value, list):
            # If the value is a list, use RPUSH to push elements to a Redis list
            r.delete(redis_key)  # Clear existing list if it exists
            r.rpush(redis_key, *value)
            print(f"Set list key: {redis_key} -> {value}")
        
        else:
            # Ignore unsupported types
            print(f"Unsupported value type for key: {key}. Only strings and lists are supported.")
    
    print("Upload completed.")

if __name__ == '__main__':
    fire.Fire(upload_to_redis)
