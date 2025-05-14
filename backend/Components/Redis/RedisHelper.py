import redis
import json

class RedisHelper:
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        self.client = redis.Redis(host=host, port=port, db=db, password=password, decode_responses=True)

    def set_value(self, key, value, ex=None):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        return self.client.set(key, value, ex=ex)

    def get_value(self, key):
        value = self.client.get(key)
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return value

    def delete_key(self, key):
        return self.client.delete(key)

    def key_exists(self, key):
        return self.client.exists(key) > 0

    def set_hash(self, key, mapping):
        return self.client.hmset(key, mapping)

    def get_hash(self, key):
        return self.client.hgetall(key)

    def push_to_list(self, key, value, left=True):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        return self.client.lpush(key, value) if left else self.client.rpush(key, value)

    def pop_from_list(self, key, left=True):
        val = self.client.lpop(key) if left else self.client.rpop(key)
        try:
            return json.loads(val)
        except (TypeError, json.JSONDecodeError):
            return val