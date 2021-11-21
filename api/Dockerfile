FROM python:3.8

RUN mkdir -p /usr/src/api
WORKDIR /usr/src/api
ADD ./requirements.txt /usr/src/api/requirements.txt

COPY . /usr/src/api

RUN pip install -r requirements.txt
ENV TZ=Europe/Moscow
