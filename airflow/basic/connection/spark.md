# spark 연결


1. Provider 설치
```bash
$ pip install apache-airflow-providers-apache-spark
```

2. spark 코드 작성

```python
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

spark = SparkSession.builder.master("local").appName("create-dataframe").getOrCreate()


stocks = [('Google', 'GOOGL', 'USA', 2984, 'USD'), 
 ('Netflix', 'NFLX', 'USA', 645, 'USD'),
 ('Amazon', 'AMZN', 'USA', 3518, 'USD'),
 ('Tesla', 'TSLA', 'USA', 1222, 'USD'),
 ('Samsung', '005930', 'Korea', 70600, 'KRW'),
 ('Kakao', '035720', 'Korea', 125000, 'KRW')]

schema = ["name", "ticker", "country", "price", "currency"]
df = spark.createDataFrame(data=stocks, schema=schema)

df.show()
# +-------+------+-------+------+--------+                                        
# |   name|ticker|country| price|currency|
# +-------+------+-------+------+--------+
# | Google| GOOGL|    USA|  2984|     USD|
# |Netflix|  NFLX|    USA|   645|     USD|
# | Amazon|  AMZN|    USA|  3518|     USD|
# |  Tesla|  TSLA|    USA|  1222|     USD|
# |Samsung|005930|  Korea| 70600|     KRW|
# |  Kakao|035720|  Korea|125000|     KRW|
# +-------+------+-------+------+--------+

usaStocksDF = df.select("name", "country", "price").where("country == 'USA'").orderBy("price")
usaStocksDF.show()
# +-------+-------+-----+
# |   name|country|price|
# +-------+-------+-----+
# |Netflix|    USA|  645|
# |  Tesla|    USA| 1222|
# | Google|    USA| 2984|
# | Amazon|    USA| 3518|
# +-------+-------+-----+

df.groupBy("currency").max("price").show()
# +--------+----------+
# |currency|max(price)|
# +--------+----------+
# |     KRW|    125000|
# |     USD|      3518|
# +--------+----------+

from pyspark.sql.functions import avg, count
df.groupBy("currency").agg(avg("price")).show()
# +--------+----------+
# |currency|avg(price)|
# +--------+----------+
# |     KRW|   97800.0|
# |     USD|   2092.25|
# +--------+----------+
df.groupBy("currency").agg(count("price")).show()
# +--------+------------+
# |currency|count(price)|
# +--------+------------+
# |     KRW|           2|
# |     USD|           4|
# +--------+------------+
```


3. dag skeleton
```python

from datetime import datetime
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {
    'start_date': datetime(2023, 1, 1)
}

with DAG(dag_id='spark-example',
         schedule_interval='@daily',
         default_args=default_args,
         tags=['spark'],
         catchup=False
    ) as dag:


    # Spark job을 실행하는 python 코드의 경로를 입력
    submit_job = SparkSubmitOperator(
        application='/home/ithingvv34/data-engineering/spark/count_trips_sql.py',
        task_id='submit_job',
        conn_id='spark_local'
    )

```

4. spark connection 설정
- `conn_id='spark_local'`


<img src="./../image/49.png">

5. dag task test

```bash
$ airflow tasks test spark-example spark_local 2023-01-01
```
<img src="./../image/50.png">
