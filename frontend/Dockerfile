FROM node:18-alpine

WORKDIR /usr/src/app

COPY package.json package-lock.json /usr/src/app/

RUN npm ci

COPY ./public /usr/src/app/public
COPY ./src /usr/src/app/src

RUN npm run build

ENV NODE_ENV production

EXPOSE 3000

CMD [ "npx", "serve", "build" ]