from config.sparkConnection import spark_session
from config.redisConnection import redis_connect
from utils.spark_utils import return_rdd
from utils.redis_utils import data_index
from redis.commands.search.query import Query
spark=spark_session()
r = redis_connect()
res=return_rdd(spark)
rs_shoe= data_index(r,res)
res=rs_shoe.search(Query("*").return_field("$.name"))
print(res)
spark.stop()
