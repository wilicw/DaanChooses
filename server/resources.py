# -*- encoding: utf8-*-
from flask_restful import Resource, reqparse
from flask import jsonify, request
import auth, config, db

db = db.connect()

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
        data = []
        if id==0:
            for item in db.clubs.find():
                data.append({'id': item['id'],
                             'name': item['name'],
                             'reject': item['reject'],
                             'year': item['year']})
            return jsonify(data)
        else:
            obj = db.clubs.find({"id": int(id)})
            for item in obj:
                data.append({
                    'id': item['id'],
                    'name': item['name'],
                    'max': item['max_students'],
                    'reject': item['reject'],
                    'teacher': item['teacher'],
                    'comment': item['comment'],
                    'location': item['location'],
                    'year': item['year']
                })
            return jsonify(data)

class Chooses(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        try:
            id = auth.identify(token.split()[1])['username']
            obj = db.chooses.find({'student': str(id)})
            index = 0
            data = []
            for item in obj:
                data.append({
                    'id': index,
                    'step': item['step'],
                    'club_id': item['club'],
                    'year': item['year']
                })
            return jsonify(data)
        except:
            return jsonify({'status': 401})
    def post(self):
        token = request.headers.get('Authorization')
        data = request.get_json()
        try:
            id = auth.identify(token.split()[1])['username']
            db.chooses.delete_many({'student': str(id)})
            for item in data:
                db.chooses.insert_one({
                    "student": str(id),
                    "club": item['club_id'],
                    "step": item['step'],
                    "year": 10801
                })
            return jsonify({'status': 200})
        except Exception as e:
            print(str(e))
            return jsonify({'status': 401})

class Users(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        try:
            id = auth.identify(token.split()[1])['username']
            data = []
            obj = db.students.find({'account': str(id)})
            obj = obj[0]
            results = []
            for result in db.results.find({'account': str(obj['account'])}):
                results.append({
                    'id': result['id'],
                    'year': result['year']
                })
            data.append({
                'id': obj['id'],
                'name': obj['student_name'],
                'class': obj['student_class'],
                'result': results
            })
            return jsonify(data)
        except Exception as e:
            print(e)
            return jsonify({'status': 401})


class DetailClub(Resource):
    def get(self, id):
        token = request.headers.get('Authorization')
        status = auth.Manageidentify(token.split()[1])
        if status:
            if int(status['permission'])>10:
                for i in range(1, config.getConf("maxchooses")+1):
                    print(i)
            return jsonify({'status': 200})
        else:
            return jsonify({'status': 401})

class SystemInfo(Resource):
    def get(self):
        return jsonify({
                'status': 200,
                'title': '大安高工選課系統',
                'maxChoose': config.getConf("maxchooses"),
                'systemAnnouncement': '系統開放時間： 8/23(五) 09:00 ~ 8/28(三) 12:00',
                'closeDate': '2020/10/31 17:00'
            })


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

class ManageNotChoose(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        status = auth.Manageidentify(token.split()[1])
        if status:
            try:
                data = []
                for i in db.students.find():
                    account = i['account']
                    n = db.chooses.count({'student': str(account)})
                    if n == 0:
                        data.append({
                            'id': i['account'],
                            'name': i['student_name'],
                            'class': i['student_class']
                        })
                return jsonify(data)
            except Exception as e:
                print(e)
                return jsonify({'status': 401})
        else:
            return jsonify({'status': 401})

class ManageGetChoose(Resource):
    def get(self, id=0):
        token = request.headers.get('Authorization')
        status = auth.Manageidentify(token.split()[1])
        if status:
            try:
                data = []
                obj = db.chooses.find()
                for i in obj:
                    data.append({
                        'club': i['club'],
                        'step': i['step']
                    })
                return jsonify(data)
            except Exception as e:
                print(e)
                return jsonify({'status': 401})
        else:
            return jsonify({'status': 401})
