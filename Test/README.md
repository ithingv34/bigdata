# Testing DAGS

**테스트가 필요한 이유**
- Dag에 정의한 작업이 예상대로 동작하는지 확인하기 위해 테스트 환경을 구축하는 것은 중요하다. 
- 테스트를 통해 버그나 에러를 사전에 찾아내고 수정할 수 있어 안정적인 작업 스케줄링을 보장하고 코드 품질을 향상할 수 있기 때문이다.
- 이 문서는 여러 환경에서 Airflow에서 Dag를 테스트하는 방법과 DAG를 작성 후 테스트를 자동화하는 과정을 실습한 내용이 담겨있다. 

**목차**
- Testing in Python
- Testing in Airflow      - DAG integrity test
- Unit testing in Airflow
- Unit testing with templated arguments
- Unit testing using mocking
- Integration testing
- DTAP environments
- CI/CD

---
### Testing in Python

파이썬에서 테스트를 위해 가장 많이되는 프레임워크는 `unittest`와 `pytest`가 있다. `unittest`는 파이썬에 내장된 기본 테스트 프레임워크이며 `pytest`는 unittest와 비교해 조금 더 간단하고 유연하게 사용이 가능한 프레임워크이다. 

**pytest 기본 사용법**

1. pytest의 특징으로는 테스트 함수의 이름이 `test_`로 시작해야하며 `assert` 구문을 사용하여 테스트 결과를 확인할 수 있다.
 
```python
def add(a: int, b: int) -> int:
    return a + b

def test_add():
    result = add(1, 2)
    assert result == 3
```

2. `@pytest.fixture` 데코레이터를 사용해 블록을 재사용할 수 있다.
   
```python
import pytest

def add(a: int, b: int) -> int:
    return a + b

@pytest.fixture
def a() -> int:
    return 1 

@pytest.fixture
def b() -> int:
    return 2

def test_add(a, b):
    assert add(a, b) == 3
```

- pytest에 대한 자세한 내용은 [공식 문서](https://docs.pytest.org/en/7.3.x/)를 참고

---
### Testing in Airflow      - DAG integrity test

- DAG 통합 테스트를 통해 DAG id가 중복, 사이클이 있는지 확인하며 required argument가 빠지지 않았는지 검사할 수 있다.

```python
from airflow.models import DagBag

def test_dagbag():
    dag_bag = DagBag(include_examples=False) # ~ (1)
    assert not bag_bag.impot_errors # ~ (2)
```
- (1): `$AIRFLOW_HOME/dags`에 있는 모든 dag를 로드
- (2): DAG 파일을 로드하는 동안 발생한 에러가 있는지 확인한다. 에러가 없으면 테스트가 통과된다

**예시**

```python
"""모든 DAG에 대한 유효성 검증"""

from airflow.models import DagBag

def test_dagbag():
    """
    Airflow의 DagBag를 이용하여 DAG 파일을 검증한다.
    이 과정에는 다음과 같은 유효성 검사가 포함된다.

    1. 태스크에 필요한 인수가 있는지
    2. DAG ID가 고유한지
    3. DAG에 사이클이 없는지
    """
    dag_bag = DagBag(include_examples=False)
    assert not dag_bag.import_errors  

    # 각 DAG에 Tag를 가지도록 강제할 수 있다.
    for dag_id, dag in dag_bag.dags.items():
        error_msg = f"{dag_id} in {dag.full_filepath} has no tags"
        assert dag.tags, error_msg
```

- (1) DAG id가 빠진 경우
- (2) Tag를 생략한 경우
- (3) Cycle이 발생한 경우
  
```python
import datetime

from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

with DAG(
    # dag_id="hello_world", ~ (1) DAG id 생략
    start_date=datetime.datetime(2021, 1, 1),
    schedule_interval=None,
    # tags=["hello", "world"], ~ (2) Tag 생략
) as dag:
    hello = BashOperator(task_id="hello", bash_command="echo 'hello'")
    world = PythonOperator(task_id="world", python_callable=lambda: print("world"))
    hello >> world >> hello # ~ (3) cycle 
```

---
### Unit testing in Airflow

- `BashOperator`를 테스트할 때는 실행 결과의 로그를 확인하여 실행이 제대로 이루어졌는지 확인할 수 있다.
- 

```python
def test_bash_operator():
    test = BashOperator(task_id="test", bash_command="echo hello")
    result = test.execute(context={})
    assert result == "hello"
```


---
### Unit testing with templated arguments


---
### Unit testing using mocking


---
### Integration testing

---
### DTAP environments


---
### CI/CD
