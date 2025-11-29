#FROM python:3.12-slim
FROM registry.cn-shenzhen.aliyuncs.com/gsmini/python:3.12-slim
LABEL maintainer=""
COPY . ./
COPY .env_prod .

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

# 环境变量配置
RUN mv .env_prod .env
EXPOSE 8000
CMD ["python","main.py"]