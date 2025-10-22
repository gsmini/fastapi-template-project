# fastapi-template-project
# 创建虚拟环境
```python
 virtualenv -p ~/.pyenv/versions/3.12.1/bin/python fastapi-template-project-env
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