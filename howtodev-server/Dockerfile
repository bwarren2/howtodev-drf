FROM python:3.8.2-alpine

RUN apk update && apk add build-base python-dev py-pip jpeg-dev zlib-dev openssl-dev gcc libffi-dev postgresql-dev autoconf automake build-essential libtool  bash
ENV LIBRARY_PATH=/lib:/usr/lib

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /usr/src/app

WORKDIR /usr/src/app/howtodev-server

# RUN python manage.py collectstatic --noinput
