#!env/bin/python
from flask import Flask, render_template
from flask_restful import Api
import auth, resources
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(resources.SystemInfo, '/api/info')
api.add_resource(resources.Login, '/api/login')
api.add_resource(resources.Clubs, '/api/clubs', '/api/clubs/', '/api/clubs/<string:id>')
api.add_resource(resources.Users, '/api/user')
api.add_resource(resources.Chooses, '/api/chooses')

api.add_resource(resources.GetNotChoosesFile, '/api/file/notchooses/<string:token>')
api.add_resource(resources.GetAllStudentsFile, '/api/file/allstudents/<string:token>')

api.add_resource(resources.ManageLogin, '/api/manage/login')
api.add_resource(resources.ManageNotChoose, '/api/manage/notchoose')
api.add_resource(resources.ManageStudents, '/api/manage/students', '/api/manage/students/', '/api/manage/students/<string:id>')
api.add_resource(resources.ManageGetChoose, '/api/manage/choose/<string:id>')
api.add_resource(resources.DetailClub, '/api/detail/club/<string:id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
