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