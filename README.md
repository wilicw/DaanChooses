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
version: '3.1'

services:
  mongo:
    image: mongo
    restart: always
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: toor
    volumes:
      - ./data:/data/db
    ports:
      - 27017:27017
  mongo-express:
    image: mongo-express
    restart: always
    ports:
      - 8081:8081
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: root
      ME_CONFIG_MONGODB_ADMINPASSWORD: toor
  app:
    build: .
    ports:
        - 8080:5000
    links:
        - mongo
```
