from pyspark.sql import SparkSession
from pyspark.sql.functions import unix_timestamp
from pyspark.sql.types import *
from multiprocessing.pool import ThreadPool

spark=SparkSession.Builder().appName("Trial app").getOrCreate()
file_list=["../dataset/7210_1.csv","../dataset/Datafiniti_Womens_Shoes_Jun19.csv","../dataset/Datafiniti_Womens_Shoes.csv"]

def read_csv(file):
    df = spark.read\
    .option("header", "true") \
    .option("delimiter", ",") \
    .option("escape",'"')\
    .csv(file)
    return df


pool = ThreadPool(10)
df_collection = pool.map(read_csv, file_list)
pool.close()
pool.join()

merged_df = df_collection[0].unionByName(df_collection[1], allowMissingColumns=True)
merged_df=merged_df.unionByName(df_collection[2],allowMissingColumns=True)
reducedf=merged_df.select(['name','dateAdded','dateUpdated','brand','categories','colors'])
reducedf=reducedf.withColumn('dateAdded',reducedf.dateAdded.cast(DateType()))
reducedf=reducedf.withColumn('dateAddedInt',unix_timestamp(reducedf.dateAdded))
reducedf=reducedf.withColumn('dateUpdated',reducedf.dateUpdated.cast(DateType()))
reducedf=reducedf.withColumn('dateUpdatedInt',unix_timestamp(reducedf.dateUpdated))
rdd=reducedf.toJSON()
res=rdd.collect()
print(res[-1])
spark.stop()