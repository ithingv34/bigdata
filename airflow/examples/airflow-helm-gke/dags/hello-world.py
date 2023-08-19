from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime

default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(2023, 4, 21),
        'retries': 0
    }

dag = DAG('git-sync-test_dag', default_args=default_args, schedule_interval='@once')

task1 = BashOperator(
        task_id='task1',
        bash_command='echo "Hello World"',
        dag=dag
    )

task2 = BashOperator(
        task_id='task2',
        bash_command='request from wsl "',
        dag=dag
    )

task1 >> task2