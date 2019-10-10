import jwt, config, models
import datetime, hashlib

session = (models.DB_session())()

users = []
def renewUsers():
    session = (models.DB_session())()
    try:
        for item in session.query(models.Students).all():
            users.append({'id': item.id,
                     'username': item.account,
                     'password': item.password})
    except:
        session.rollback()

def authenticate(username, password):
    renewUsers()
    for i in users:
        if i['username'] == username and i['password'] == password:
             encoded = jwt.encode({
                    'username': username,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=14400)
                }, config.getConf('jwtsecret'), algorithm='HS256')
                # 4 hours token available
             return encoded
    return False

def identify(token):
    data = jwt.decode(token, config.getConf('jwtsecret'), algorithms=['HS256'])
    return data

def Manageauthenticate(username, password):
    session = (models.DB_session())()
    for i in session.query(models.Manage).filter(models.Manage.account == username).all():
        if i.password == hashlib.sha256(password.encode('utf-8')).hexdigest():
             encoded = jwt.encode({
                    'username': username,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=7200)
                }, config.getConf('jwtsecret'), algorithm='HS256')
                # 2 hours token available
             return encoded
    return False

def Manageidentify(token):
    try:
        data = jwt.decode(token, config.getConf('jwtsecret'), algorithms=['HS256'])
    except:
        return False
    username = data['username']
    session = (models.DB_session())()
    for i in session.query(models.Manage).filter(models.Manage.account == username).all():
        return {"permission": i.permission}
    return False
