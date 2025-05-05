FROM node:20-alpine

LABEL maintainer="Ad.BadiDesign@gmail.com"

WORKDIR /usr/src/ui

RUN apk update

COPY ./ui/package*.json ./

RUN npm install

COPY ./ui .

EXPOSE 3000

