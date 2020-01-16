import pymongo, config
def connect():
    host = config.getConf("dbhost")
    port = config.getConf("dbport")
    username = config.getConf("dbaccount")
    password = config.getConf("dbpassword")
    client = pymongo.MongoClient('mongodb://{}:{}@{}:{}/?authSource=DaanChooses'.format(username, password, host, port))
    return client.DaanChooses