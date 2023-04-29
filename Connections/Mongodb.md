# MongoDB 연결

**1. MongoDB 클러스터 생성 및 연결** 

```
# 패키지 색인 업데이트
$ sudo apt update

# 의존성 항목 설치
$ sudo apt install wget gpg

# MongoDB 공개 키를 가져옴
$ wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# 패키지 관리자 소스에 MongoDB 리포지토리 추가
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# 업데이트
sudo apt update

# mongodb connect
$ mongosh "mongodb+srv://cluster0.uvvyu7p.mongodb.net/mydb" --apiVersion 1 --username admin

# db 사용
$ [primary] mydb> use mydb

# "test" collection 생성
$ [primary] mydb> db.createCollection("test")
{ ok: 1 }


```
<img src="./../image/9.png">

**2. MongoDB 연결을 위한 패키지 설치**

```bash
pip install apache-airflow-providers-mongo
```

**3. MongoDB 설정**
- MongoDB Atlas 사용

<img src="./../image/52.png">

**4. DAG 작성**

```python
import json
from datetime import datetime
from airflow import DAG
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.operators.python import PythonOperator

default_args = {
    'start_date': datetime(2023, 1, 1),
}

def upload_mongo():
    try:
        mongo_hook = MongoHook(conn_id='mongo_id')
        my_client = mongo_hook.get_conn()
        mydb = my_client.mydb
        mycol = mydb.test

        print(f"Connected to MongoDB - {my_client.server_info()}")
        
        ########## 삽입 ###########
        my_dict = [
            {'category' : 'nosql', 'name' : 'redis'},
            {'category' : 'nosql', 'name' : 'mongodb'},
            {'category' : 'nosql', 'name' : 'cassandra'},
            {'category' : 'nosql', 'name' : 'hbase'}
        ]

        mycol.insert_many(my_dict)

        ########## 쿼리 ###########
        cols = mycol.find()

        for col in cols:
            print(col)

    except Exception as e:
        print("Error to MongoDB -- {e}")

with DAG(dag_id='mongo_hook_check',
         schedule_interval='@daily',
         default_args=default_args,
         tags=['mongodb'],
         catchup=False
    ) as dag:


    t1 = PythonOperator(
        task_id='upload-mongodb',
        python_callable=upload_mongo,
        dag=dag
        )

    t1

```

**5. DAG 테스트**

```bash
$ airflow tasks test mongo_hook_check upload-mongodb 2023-01-01
```
<img src="./../image/51.png">