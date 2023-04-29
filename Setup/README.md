# 목차
- pip를 활용한 로컬 Airflow 구축
- docker-compose를 활용한 Airflow 구축


---
### pip를 활용한 로컬 Airflow 구축

**airflow 설치 - pip**
```python
# airflow 설치
$ pip install apache-airflow

# airflow 홈
$ export AIRFLOW_HOME=~/airflow
```

**airflow db init**
```python

# airflow 데이터베이스 초기화
$ airflow db init
```

**airflow 설치 후 어드민 생성**
```python
# 관리자 권한 생성
$ airflow users create \
    --username admin \
    --password admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email ithingv34@gmail.com
```

**airflow 유저 확인**
```python
$ airflow users list
```
<img src="./../image/39.png">


**airflow 설치 후 웹 인터페이스 실행**
```
$ airflow webserver -p 8080 

# 백그라운드로 실행
$ airflow webserver -p 8080 -D

# 프로세스 종료 시
$ sudo kill -9 $(sudo lsof -t -i:8080)
```
- 시간 설정 - `KST`
<img src="./../image/1.png">

**airflow 설치 후 스케줄러 실행**
```python
$ airflow scheduler
```

**airflow 기본 dags 출력**
```python
$ airflow dags list
```
<img src="./../image/40.png">

**dag내의 task 출력**
- `example_xcom`
```python
$ airflow tasks list example_xcom
```
<img src="./../image/41.png">

**dag를 실행시키는 trigger**
```python
$ airflow dags trigger -e 2022-01-01 example_xcom
```
<img src="./../image/42.png">

**airflow 환경설정**
```
$ airflow.cfg
```

**Hello Airflow 만들기**
- DAG의 위치 - `~/airflow/dags`
```python
from datetime import timedelta

import pendulum
from airflow.models import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="hello_dag_v1",
    schedule_interval='1 * * * *',
    dagrun_timeout=timedelta(minutes=1),
    start_date=pendulum.datetime(2023, 2, 15, tz="Asia/Seoul"),
    max_active_runs=1,
    max_active_tasks=1,
    catchup=False
) as dag:
    bash_operator = BashOperator(
    task_id="hell_task",
    bash_command="echo Hello, Airflow",
    )

bash_operator
```
---