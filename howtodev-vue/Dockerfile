FROM node:13.8.0-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apk update && apk add bash

ENV PATH /usr/src/app/node_module/.bin:$PATH

COPY package.json /usr/src/app/package.json

RUN npm install
RUN npm install -g @vue/cli

COPY . /usr/src/app
