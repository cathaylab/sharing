import numpy.random as rnd
from pyspark.sql import SparkSession

DATA_PATH = 'outputs'

spark = SparkSession \
    .builder \
    .appName("Pyspark entry point") \
	.master("local[*]") \
	.getOrCreate()

output_path = '{}/{}'.format(DATA_PATH, rnd.randint(100000)) 
print("Start dump df to {}".format(output_path))
spark.sql("show databases").write.mode("overwrite").parquet(output_path)
print("Finish write dataframe!")

spark.stop()
