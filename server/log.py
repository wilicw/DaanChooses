import db, datetime

db = db.connect()


def Log(account, method, ua, ip):
    db.log.insert({
        "account": account,
        "method": method,
        "ua": ua,
        "ip": ip,
        "time": datetime.datetime.now(),
    })
