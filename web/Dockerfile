FROM node:alpine as base
MAINTAINER Jack Greenberg <jgreenberg@olin.edu>

WORKDIR /web

COPY package.json yarn.lock ./
RUN ["yarn", "install"]

FROM node:alpine as build
WORKDIR /web

COPY --from=base /web/node_modules /web/node_modules

COPY . /web

RUN ["yarn", "build"]

CMD ["sh", "/web/scripts/entrypoint.sh"]
