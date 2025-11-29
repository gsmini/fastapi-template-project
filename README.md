# fastapi-template-project

fastapi + sqlalchemy orm + celery 完整案例 celery任务 celery 定时任务 docker 部署
## 全局返回体
```json
{
    "code": 0,
    "message": "request succeed",
    "data": {},
    "request_id": "caccd938-b8e1-435f-96d3-14e29d0291d1"
}
```

# 如何使用
## 创建虚拟环境

```shell
virtualenv - p ~/.pyenv/versions/3.12.1/bin/python fastapi-template-project-env
source fastapi-template-project-env/bin/active
```

## 数据库创建

### 业务数据库 mysql

```shell
docker run -p 3306:3306 --name fastapi-template-project-mysql -e MYSQL_ROOT_PASSWORD=root -d registry.cn-shenzhen.aliyuncs.com/gsmini/mysql:5.7
docker exec -it fastapi-template-project-mysql /bin/bash
mysql -u root -p
CREATE DATABASE fastapi-template-project CHARSET=utf8mb4;
```

### 业务数据库 redis

```shell
docker run -p 6379:6379 --name fastapi-template-project-redis  -d registry.cn-shenzhen.aliyuncs.com/gsmini/redis:7
```

# 本地启动

## web服务

```shell
python main.py 
```

## celery

```shell
celery -A celery_app.celery_app  worker -l info   

```

# docker 部署

## web
```shell
docker build . -t fastapi-template:v6
docker run -p 8000:8000  fastapi-template:v6
```

## celery异步任务
```shell
docker build . -t fastapi-template-celery:v1   -f Dockerfile_Celery 
docker run fastapi-template-celery:v1
```


## celery 定时任务（方式1）

```shell
docker build . -t fastapi-template-celery-beat:v1   -f Dockerfile_Celery_Beat
docker run fastapi-template-celery-beat:v1
```
> celery worker和beat 任务修改后需要同时部署 否则可能导致代码不一致task任务无法识别等其他错误
## python scheduler 定时任务(方式2)

```shell
docker build . -t fastapi-template-scheduler:v1   -f Dockerfile_Scheduler 
docker run fastapi-template-scheduler:v1
```
