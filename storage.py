import os
import json

try:
    import redis
    DEFAULT_STORAGE_MODE = 'redis'
except ImportError:
    print("Redis not available")
    try:
        from deta import Deta
        print("Using Deta as default storage")
        DEFAULT_STORAGE_MODE = 'deta'
    except ImportError:
        print("Deta base not available")
        pass


class RedisStorageMode():
    redis = None
    def __init__(self, tag):
        self.tag = tag
        if RedisStorageMode.redis is None:
            RedisStorageMode.redis = redis.Redis.from_url(
                os.getenv('REDIS_URL'),
                encoding="utf-8",
                decode_responses=True
            )

    def set(self, data: dict = None, key: str = None):
        self.redis.hset(name=self.tag, key=key, value=json.dumps(data))

    def get(self, key: str):
        value = self.redis.hget(name=self.tag, key=key)
        
        if value is not None:
            value = json.loads(value)

        return value
    
    def delete(self, key: str):
        self.redis.hdel(self.tag, key)


class DetaStorageMode:
    def __init__(self, tag):
        self.tag = tag
        self.base = Deta().Base(tag)

    def set(self, data: dict = None, key: str = None):
        self.base.put(data=data, key=key)

    def get(self, key: str):
        return self.base.get(key)
    
    def delete(self, key: str):
        self.base.delete(key)


STORAGE_MODES = {
    'redis': RedisStorageMode,
    'deta': DetaStorageMode
}


class Storage:
    @staticmethod
    def client(tag='default', mode=DEFAULT_STORAGE_MODE):
        return STORAGE_MODES[mode](tag)
