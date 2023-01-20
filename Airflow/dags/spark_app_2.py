import pyspark
import os
from pyspark.sql import SparkSession


spark = SparkSession \
        .builder \
        .master("local").appName("PySpark_Postgres_test").getOrCreate()
df = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://host.docker.internal:5432/airflow") \
        .option("driver", "org.postgresql.Driver") \
        .option("dbtable", "newtable") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .load()
df.printSchema()