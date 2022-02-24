FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1
RUN mkdir app
RUN mkdir /run/daphne/

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r ./requirements.txt

COPY . /app


