import json

def getConf(name):
    with open('../app.conf.json') as json_data:
        d = json.load(json_data)
        return d[name]
