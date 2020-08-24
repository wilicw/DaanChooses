import jwt, config, db
import datetime, hashlib

db = db.connect()

def authenticate(username, password):
    obj = db.students.find_one({'account': str(username)})
    if obj is not None and obj != '' and obj['password'] == password and obj['enable'] == 1:
        encoded = jwt.encode({
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=14400)
        }, config.getConf('jwtsecret'), algorithm='HS256')
        # 4 hours token available
        return encoded
    else:
        return False

def identify(token):
    data = jwt.decode(token, config.getConf('jwtsecret'), algorithms=['HS256'])
    return data

def Manageauthenticate(username, password):
    obj = db.manage.find_one({'username': str(username)})
    if obj is not None and obj['password'] == hashlib.sha256(password.encode('utf-8')).hexdigest():
        encoded = jwt.encode({
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=7200)
        }, config.getConf('jwtsecret'), algorithm='HS256')
        # 2 hours token available
        return encoded
    else:
        return False

def Manageidentify(token):
    try:
        data = jwt.decode(token, config.getConf('jwtsecret'), algorithms=['HS256'])
    except:
        return False
    username = data['username']
    obj = db.manage.find_one({'username': str(username)})
    if obj:
        return {'permission': obj['permission']}
    else:
        return False
