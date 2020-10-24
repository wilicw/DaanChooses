import pymongo, config, redis


def connect():
    host = config.getConf("dbhost")
    port = int(config.getConf("dbport"))
    username = config.getConf("dbaccount")
    password = config.getConf("dbpassword")
    client = pymongo.MongoClient(
        "mongodb://{}:{}@{}:{}/?authSource=DaanChooses".format(
            username, password, host, port))
    return client.DaanChooses


def r():
    r = redis.Redis(
        host=config.getConf("redishost"),
        port=config.getConf("redisport"),
        password=config.getConf("redispassword"),
    )
    return r
