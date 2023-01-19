import pyspark
import os
from pyspark.sql import SparkSession
from pyspark.sql import Row

# path = '/opt/airflow/'
# name = "postgresql-42.5.1.jar"
# for root, dirs, files in os.walk(path):
#         if name in files:
#                 app_path = (os.path.join(root, name))
#                 break
spark = SparkSession \
        .builder \
        .config("spark.jars", "/tmp/postgresql-42.5.1.jar") \
        .config("spark.executor.extraClassPath", "/tmp/postgresql-42.5.1.jar") \
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