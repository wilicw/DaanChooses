# -*- encoding: utf8-*-
from flask_restful import Resource, reqparse
from flask import jsonify, request, send_from_directory
import auth, config, db, json
from pyexcel_ods import save_data
from collections import OrderedDict
from threading import Thread

redis = db.r()
db = db.connect()

class Login(Resource):
    def get(self):
        token = request.headers.get("Authorization")
        try:
            id = auth.identify(token.split()[1])["username"]
            print(id)
            return jsonify({"status": 200})
        except:
            return jsonify({"status": 401})

    def post(self):
        data = request.get_json()
        token = auth.authenticate(str(data["username"]), str(data["password"]))
        if token:
            return jsonify({"status": 200, "token": str(token).split("'")[1]})
        else:
            return jsonify({"status": 401})

class Clubs(Resource):        
    def get(self, id=0):
        if id==0:
            data = redis.get("all")
            year = config.year()
            def getAllData():
                data = []
                for item in db.clubs.find({"year": year}):
                    data.append({"id": item["id"],
                        "name": item["name"],
                        "reject": item["reject"],
                        "student_year": item["student_year"],
                        "classification": item["classification"],
                        "year": item["year"]
                    })
                redis.set("all", json.dumps(data))
            if data == None or len(data) == 0:
                getAllData()
            else:
                thread = Thread(target=getAllData)
                thread.start()
            return jsonify(json.loads(redis.get("all")))
        else:
            id = int(id)
            data = redis.get("club{}".format(id))
            def getClub(id):
                data = []
                obj = db.clubs.find({"id": id})
                for item in obj:
                    data.append({
                        "id": item["id"],
                        "name": item["name"],
                        "max": item["max_students"],
                        "reject": item["reject"],
                        "teacher": item["teacher"],
                        "comment": item["comment"],
                        "classification": item["classification"],
                        "location": item["location"],
                        "year": item["year"]
                    })
                redis.set("club{}".format(id), json.dumps(data))
            if data == None or len(data) == 0:
                getClub(id)
            else:
                thread = Thread(target=getClub(id))
                thread.start()
            return jsonify(json.loads(redis.get("club{}".format(id))))

class Chooses(Resource):
    def get(self):
        token = request.headers.get("Authorization")
        year = config.year()
        try:
            id = auth.identify(token.split()[1])["username"]
            obj = db.students.find_one({
                    "account": str(id)
                })
            index = 0
            data = []
            if obj is not None:
                for item in obj["chooses"]:
                    if item["year"] != year:
                        continue
                    data.append({
                        "id": index,
                        "step": item["step"],
                        "club_id": item["club"],
                        "year": item["year"]
                    })
            return jsonify(data)
        except Exception as e:
            print(str(e))
            return jsonify({"status": 401})
    def post(self):
        token = request.headers.get("Authorization")
        data = request.get_json()
        year = config.year()
        try:
            id = auth.identify(token.split()[1])["username"]
            db.students.update_one({
                    "account": str(id)
                }, {
                    "$pull": {
                        "chooses": {
                            "year": year
                        }
                    }
                })
            for item in data:
                db.students.update_one({"account": str(id)}, {
                    "$push": {
                        "chooses": {
                            "club": int(item["club_id"]),
                            "step": int(item["step"]),
                            "year": year
                        }
                    } 
                })
            return jsonify({"status": 200})
        except Exception as e:
            print(str(e))
            return jsonify({"status": 401})

class Users(Resource):
    def get(self):
        token = request.headers.get("Authorization")
        try:
            id = auth.identify(token.split()[1])["username"]
            data = []
            obj = db.students.find_one({"account": str(id)})
            results = []
            for result in obj["results"]:
                results.append({
                    "id": result["club"],
                    "year": result["year"]
                })
            data.append({
                "id": obj["id"],
                "name": obj["student_name"],
                "class": obj["student_class"],
                "result": results,
                "year": obj["year"]
            })
            return jsonify(data)
        except Exception as e:
            print(e)
            return jsonify({"status": 401})


class DetailClub(Resource):
    def get(self, id):
        token = request.headers.get("Authorization")
        status = auth.Manageidentify(token.split()[1])
        if status:
            if int(status["permission"])>10:
                for i in range(1, config.getConf("maxchooses")+1):
                    print(i)
            return jsonify({"status": 200})
        else:
            return jsonify({"status": 401})

class SystemInfo(Resource):
    def get(self):
        setting = db.config.find_one({"id": 0})
        print(setting)
        if setting is not None:
            return jsonify({
                "status": 200,
                "title": setting["title"],
                "maxChoose": int(setting["maxChoose"]),
                "systemAnnouncement": setting["systemAnnouncement"],
                "closeDate": setting["closeDate"],
                "year": setting["year"]
            })
    def post(self):
        data = request.get_json()
        token = request.headers.get("Authorization")
        status = auth.Manageidentify(token.split()[1])
        if status:
            data["id"] = 0
            db.config.delete_one({"id": 0})
            db.config.insert_one(data)
            return jsonify({"status": 200})
        else:
            return jsonify({"status": 401})

class ManageLogin(Resource):
    def get(self):
        token = request.headers.get("Authorization")
        status = auth.Manageidentify(token.split()[1])
        if status:
            print(status)
            return jsonify({"status": 200})
        else:
            return jsonify({"status": 401})
    def post(self):
        data = request.get_json()
        token = auth.Manageauthenticate(str(data["username"]), str(data["password"]))
        if token:
            return jsonify({"status": 200, "token": str(token).split("'")[1]})
        else:
            return jsonify({"status": 401})

class ManageNotChoose(Resource):
    def get(self):
        token = request.headers.get("Authorization")
        status = auth.Manageidentify(token.split()[1])
        if status:
            try:
                data = []
                year = config.year()
                obj = db.students.find()
                for item in obj:
                    count = 0
                    if item["enable"] != 1:
                        continue
                    for i in item["chooses"]:
                        if i["year"] == year:
                            count += 1
                    if count == 0:
                        data.append({
                            "id": item["account"],
                            "name": item["student_name"],
                            "class": item["student_class"]
                        })
                return jsonify(data)
            except Exception as e:
                print(e)
                return jsonify({"status": 401})
        else:
            return jsonify({"status": 401})

class GetNotChoosesFile(Resource):
    def get(self):
        year = config.year()
        obj = db.students.find()
        data = []
        table = OrderedDict()
        data.append(["學號", "班級", "姓名"])
        for item in obj:
            count = 0
            if item["enable"] != 1:
                continue
            for i in item["chooses"]:
                if i["year"] == year:
                    count += 1
            if count == 0:
                data.append([item["account"], item["student_class"], item["student_name"]])
        table.update({"Sheet 1": data})
        save_data("/tmp/tables.ods", table)
        return send_from_directory('/tmp', "tables.ods", as_attachment=True, mimetype='application/file', attachment_filename="{}分發.ods".format(year))

class ManageStudents(Resource):
    def get(self):
        token = request.headers.get("Authorization")
        status = auth.Manageidentify(token.split()[1])
        if status:
            try:
                data = []
                for stu in db.students.find({"year": (int(config.year()/100) + 3)}):
                    print(stu)
                return jsonify(data)
            except Exception as e:
                print(e)
                return jsonify({"status": 401})
        else:
            return jsonify({"status": 401})

class ManageGetChoose(Resource):
    def get(self, id=0):
        token = request.headers.get("Authorization")
        status = auth.Manageidentify(token.split()[1])
        if status:
            try:
                data = []
                obj = db.chooses.find()
                for i in obj:
                    data.append({
                        "club": i["club"],
                        "step": i["step"]
                    })
                return jsonify(data)
            except Exception as e:
                print(e)
                return jsonify({"status": 401})
        else:
            return jsonify({"status": 401})

