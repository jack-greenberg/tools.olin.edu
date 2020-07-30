FROM node:alpine

RUN mkdir /web
WORKDIR /web

COPY package.json ./
RUN yarn install

COPY . ./

RUN ["yarn", "build"]

CMD ["yarn", "run", "start"]
