from config.sparkConnection import spark_session
from config.redisConnection import redis_connect
from config.elasticConnection import elastic_connect
from utils.spark_utils import return_rdd
from utils.redis_utils import write_redis
from utils.elastic_utils import write_elastic

def main():
    """
    Integrating all the custom functions to load the csv files and write it to Redis
    """
    spark=spark_session()
    r = redis_connect()
    elastic_client= elastic_connect()
    res=return_rdd(spark)
    write_redis(r,res)
    write_elastic(elastic_client,res)
    spark.stop()

if __name__=='__main__':
    main()