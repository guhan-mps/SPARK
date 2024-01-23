from pyspark.sql import SparkSession
def spark_session()->SparkSession:
    """
    Starts a spark session
    """
    spark = SparkSession.Builder() \
    .appName("Spark Writer") \
    .getOrCreate()
    return spark
    # .master('local[*]') \
    # .config("spark.redis.host", "redis-stack-server") \
    # .config("spark.redis.port", "6379") \