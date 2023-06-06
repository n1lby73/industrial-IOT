from flask_login import current_user, login_user, logout_user
from flask_restful import Resource
from webApp import login
from webApp import api

@login.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

class indexApi(Resource):
    def get(self):
        if current_user.is_authenticated:
            return {'hello': 'world'}
        return "nah"

class loginApi(Resource):
    def get(self):
      return "X"
    def post(self):
        return "T"

api.add_resource(loginApi, '/api/login')
api.add_resource(indexApi, '/api')
