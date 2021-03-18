import redis
REDIS_PORT = 6379
REDIS_HOST = '127.0.0.1'

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
