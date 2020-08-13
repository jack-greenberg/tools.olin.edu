FROM node:alpine as base
MAINTAINER Jack Greenberg <jgreenberg@olin.edu>

WORKDIR /web

COPY package.json ./
RUN ["yarn", "install"]

FROM node:alpine as build
WORKDIR /web

COPY --from=base /web/node_modules /web/node_modules

COPY . /web/

RUN ["yarn", "build"]

CMD ["yarn", "run", "start"]
