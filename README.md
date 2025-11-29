# fastapi-template-project
# 创建虚拟环境
```python
 virtualenv -p ~/.pyenv/versions/3.12.1/bin/python fastapi-template-project-env
```



# 数据库创建

## 业务数据库 mysql

```shell
docker run -p 3306:3306 --name fastapi-template-project-mysql -e MYSQL_ROOT_PASSWORD=root -d registry.cn-shenzhen.aliyuncs.com/gsmini/mysql:5.7
docker exec -it fastapi-template-project-mysql /bin/bash
mysql -u root -p
CREATE DATABASE fastapi-template-project CHARSET=utf8mb4;
```

 

## 业务数据库 redis

```shell
docker run -p 6379:6379 --name fastapi-template-project-redis  -d registry.cn-shenzhen.aliyuncs.com/gsmini/redis:7
```
# 启动

```python
python main.py 
```


# docker build 
```python
docker build . -t fastapi-template:v1
docker run -p 8000:8000  fastapi-template:v1
```

