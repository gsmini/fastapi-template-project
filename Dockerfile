FROM python:3.12-slim

LABEL maintainer=""
RUN mkdir "/code"
WORKDIR /code
COPY requirements.txt .

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

COPY ./ .
EXPOSE 8000
CMD ["python","main.py"]