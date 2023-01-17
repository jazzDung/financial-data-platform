
from pyspark import SparkContext

sc = SparkContext("local", "First App")
    
data = [{"Category": 'A', "ID": 1, "Value": 121.44, "Truth": True},
        {"Category": 'B', "ID": 2, "Value": 300.01, "Truth": False},
        {"Category": 'C', "ID": 3, "Value": 10.99, "Truth": None},
        {"Category": 'E', "ID": 4, "Value": 33.87, "Truth": True}]
    
df = sc.parallelize(data)
df = df.collect()

print(df)