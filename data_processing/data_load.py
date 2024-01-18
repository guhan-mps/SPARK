from config.sparkConnection import spark_session
from config.redisConnection import redis_connect
from utils.spark_utils import return_rdd
from utils.redis_utils import write_redis

def main():
    """
    Integrating all the custom functions to load the csv files and write it to Redis
    """
    spark=spark_session()
    r = redis_connect()
    res=return_rdd(spark)
    write_redis(r,res)
    spark.stop()

if __name__=='__main__':
    main()