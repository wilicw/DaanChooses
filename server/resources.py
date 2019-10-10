# -*- encoding: utf8-*-
from flask_restful import Resource, reqparse
from flask import jsonify, request
import auth, models, config

class Login(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        try:
            id = auth.identify(token.split()[1])['username']
            print(id)
            return jsonify({'status': 200})
        except:
            return jsonify({'status': 401})

    def post(self):
        data = request.get_json()
        token = auth.authenticate(str(data['username']), str(data['password']))
        if token:
            return jsonify({'status': 200, 'token': str(token).split("'")[1]})
        else:
            return jsonify({'status': 401})

class Clubs(Resource):
    def get(self, id=0):
        session = (models.DB_session())()
        if id==0:
            data = []
            for item in session.query(models.Clubs).all():
                data.append({'id': item.id,
                             'name': item.name,
                             'reject': item.reject})
            return jsonify(data)
        else:
            data = []
            for item in session.query(models.Clubs).filter(models.Clubs.id == id).all():
                data.append({'id': item.id,
                             'name': item.name,
                             'max': item.max,
                             'reject': item.reject,
                             'teacher': item.teacher,
                             'comment': item.comment,
                             'location': item.location})
            return jsonify(data)

class Chooses(Resource):
    def get(self):
        session = (models.DB_session())()
        token = request.headers.get('Authorization')
        try:
            id = auth.identify(token.split()[1])['username']
            stuID = ""
            for item in session.query(models.Students).filter(models.Students.account == id).all():
                stuID = item.id
            data = []
            for item in session.query(models.Chooses).filter(models.Chooses.stu_id == stuID).all():
                data.append({'id': item.id,
                             'step': item.step,
                             'club_id': item.club_id})
            return jsonify(data)
        except:
            return jsonify({'status': 401})
    def post(self):
        session = (models.DB_session())()
        token = request.headers.get('Authorization')
        data = request.get_json()
        try:
            id = auth.identify(token.split()[1])['username']
            stuID = ""
            for item in session.query(models.Students).filter(models.Students.account == id).all():
                stuID = item.id
            session.query(models.Chooses).filter(models.Chooses.stu_id == stuID).delete()
            for item in data:
                obj = models.Chooses(stu_id=stuID, step=item['step'], club_id=item['club_id'])
                session.add(obj)
            session.commit()
            return jsonify({'status': 200})
        except:
            return jsonify({'status': 401})

class Users(Resource):
    def get(self):
        session = (models.DB_session())()
        token = request.headers.get('Authorization')
        try:
            id = auth.identify(token.split()[1])['username']
            data = []
            for item in session.query(models.Students).filter(models.Students.account == id).all():
                data.append({'id': item.id,
                             'name': item.name,
                             'class': item.Sclass,
                             'result': item.result})
            return jsonify(data)
        except:
            return jsonify({'status': 401})

class ManageLogin(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        status = auth.Manageidentify(token.split()[1])
        if status:
            print(status)
            return jsonify({'status': 200})
        else:
            return jsonify({'status': 401})
    def post(self):
        data = request.get_json()
        token = auth.Manageauthenticate(str(data['username']), str(data['password']))
        if token:
            return jsonify({'status': 200, 'token': str(token).split("'")[1]})
        else:
            return jsonify({'status': 401})

class DetailClub(Resource):
    def get(self, id):
        token = request.headers.get('Authorization')
        status = auth.Manageidentify(token.split()[1])
        if status:
            if int(status['permission'])>10:
                session = (models.DB_session())()
                for i in range(1, config.getConf("maxchooses")+1):
                    print(i)
            return jsonify({'status': 200})
        else:
            return jsonify({'status': 401})
