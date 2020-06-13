FROM node:alpine AS build
WORKDIR /app
ADD cli/package.json .
RUN npm install
ADD cli .
RUN npm run build

FROM python:slim
RUN apt-get clean \
    && apt-get -y update
RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential
COPY --from=build /tmp/dist /app/cli/dist
WORKDIR /app/server
ADD server/requirements.txt .
RUN python3 -m pip install -r requirements.txt --src /usr/local/src
COPY server .
COPY production/nginx.conf /etc/nginx
RUN chmod +x ./startup.sh
CMD ["./startup.sh"]
