FROM node:alpine AS build
WORKDIR /app
ADD ui/package.json .
RUN npm install --production
RUN npm install -g vue
ADD ui .
RUN npm run build

FROM alpine:latest
WORKDIR /app/server
RUN apk update
RUN apk add nginx
RUN apk add gcc
RUN apk add libc-dev 
RUN apk add linux-headers
RUN apk add python3-dev
RUN apk add py-pip
ADD server/requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --src /usr/local/src
COPY server .
COPY production/nginx.conf /etc/nginx
RUN addgroup -S www && adduser -S www-data -G www
RUN chmod +x ./startup.sh
COPY --from=build /tmp/dist /app/cli/dist
CMD ["./startup.sh"]
