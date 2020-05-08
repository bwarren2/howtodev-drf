FROM node:13.8.0-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apk update && apk add bash

ENV PATH /usr/src/app/node_module/.bin:$PATH

COPY package.json /usr/src/app/package.json

RUN yarn install
RUN yarn global add @vue/cli

COPY . /usr/src/app
