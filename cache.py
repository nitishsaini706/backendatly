import redis
import json

class Cache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def get(self, key: str):
        value = self.client.get(key)
        if value:
            return json.loads(value)  # Deserialize JSON string to Python object
        return None

    def set(self, key: str, value: dict):
        self.client.set(key, json.dumps(value))  # Serialize Python object to JSON string
