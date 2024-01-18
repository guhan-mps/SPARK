from redis import Redis

def redis_connect()->Redis:
    """Makes connection to the redis server"""
    r = Redis(host="localhost", port=6379, db=0, decode_responses=True)
    return r