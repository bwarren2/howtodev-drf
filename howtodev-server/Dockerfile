FROM python:3.8.2-alpine

RUN apk update && apk add build-base python-dev py-pip jpeg-dev zlib-dev \
    openssl-dev gcc libffi-dev postgresql-dev autoconf automake alpine-sdk \
    libtool bash curl

# Install node
RUN apk add --update nodejs nodejs-npm

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /usr/src/app

WORKDIR /usr/src/app/howtodev-server

