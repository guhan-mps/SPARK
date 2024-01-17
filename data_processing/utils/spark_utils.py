from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import unix_timestamp
from typing import List
def return_rdd(spark: SparkSession)->List[str]:
    base_ds = spark.read \
    .option("header", "true") \
    .option("delimiter", ",") \
    .csv(["./dataset/Datafiniti_Womens_Shoes.csv","./dataset/Datafiniti_Womens_Shoes_Jun19.csv"])
    reducedf = base_ds.select(['name','dateAdded','dateUpdated','brand','categories','colors'])
    reducedf=reducedf.withColumn('dateAdded',reducedf.dateAdded.cast(DateType()))
    reducedf=reducedf.withColumn('dateAddedInt',unix_timestamp(reducedf.dateAdded))
    reducedf=reducedf.withColumn('dateUpdated',reducedf.dateUpdated.cast(DateType()))
    reducedf=reducedf.withColumn('dateUpdatedInt',unix_timestamp(reducedf.dateUpdated))
    rdd=reducedf.toJSON()
    res=rdd.collect()
    return res