FROM node:alpine AS build
WORKDIR /app
ADD ui/package.json .
RUN npm install
ADD ui .
RUN npm run build

FROM alpine
RUN apk update
RUN apk add nginx
RUN apk add gcc
RUN apk add libc-dev 
RUN apk add linux-headers 
RUN apk add python3-dev
RUN apk add openrc
COPY --from=build /tmp/dist /app/cli/dist
WORKDIR /app/server
ADD server/requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --src /usr/local/src
COPY server .
COPY production/nginx.conf /etc/nginx
RUN addgroup -S www && adduser -S www-data -G www
RUN chmod +x ./startup.sh
CMD ["./startup.sh"]
