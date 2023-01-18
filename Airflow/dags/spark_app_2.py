import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import Row
spark = SparkSession \
        .builder \
        .config("spark.jars", "/tmp/postgresql-42.5.1.jar") \
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