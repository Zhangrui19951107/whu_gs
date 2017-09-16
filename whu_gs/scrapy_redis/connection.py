import redis
from rediscluster import StrictRedisCluster

# Default values.
REDIS_URL = None
REDIS_HOST = 'localhost'
REDIS_PORT = 6379


def from_settings(settings):
    url = settings.get('REDIS_URL',  REDIS_URL)
    host = settings.get('REDIS_HOST', REDIS_HOST)
    port = settings.get('REDIS_PORT', REDIS_PORT)
    startup_nodes=[{"host": host,"port": port}]
    return StrictRedisCluster(startup_nodes=startup_nodes)
    # REDIS_URL takes precedence over host/port specification.
   # if url:
    #    return redis.from_url(url)
    #else:
     #   return redis.Redis(host=host, port=port)
