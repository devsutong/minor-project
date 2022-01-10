FROM python:3.7-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir app

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

ADD . /app

