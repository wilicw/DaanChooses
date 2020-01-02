# DaanChoose
## Use Flask python3

### Requirements

- python 3
- nodejs
- npm (yarn)
- pip3
- docker

### Get started

Clone this project

```
$ git clone git@github.com:daancsc/DaanChoose-Flask.git
```

### Docker

#### Docker Compose example

```
version: "2"

services:
  db:
      image: mariadb
      container_name: mariadb
      restart: always
      environment:
          MYSQL_ROOT_PASSWORD: password
      volumes:
          - ./database:/var/lib/mysql
  chooseBack:
      image: chooseback
      build:
          context: ./server
      container_name: chooseBack
      restart: always
      ports:
          - "8089:5000"
      links:
          - db
  chooseFront:
      image: choosefront
      build:
          context: ./cli
          args:
            - publicPath=/choose
            - apiPath=127.0.0.1:8089
      container_name: chooseFront
      restart: always
      ports:
          - "8088:8080"

```
