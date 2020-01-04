import json, db

def getConf(name):
    with open('app.conf.json') as json_data:
        d = json.load(json_data)
        return d[name]

def year():
    d = db.connect()
    obj = d.config.find_one({"id": 0})
    return int(obj["year"])