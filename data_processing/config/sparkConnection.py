from pyspark.sql import SparkSession

def spark_session()->SparkSession:
    spark = SparkSession.Builder() \
    .master('local[*]') \
    .config("spark.redis.host", "localhost") \
    .config("spark.redis.port", "6379") \
    .appName("Spark Writer") \
    .getOrCreate()
    return spark
