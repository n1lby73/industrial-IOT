from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user
from flask_restful import Resource, reqparse
from webApp.models import users, esp32
from webApp import login, api

@login.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

class indexApi(Resource):
    def get(self):
        if current_user.is_authenticated:
            return {'hello': 'world'}

        return "user not authorized"

class loginApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("email", required=True)
        self.parser.add_argument("password", required=True)
    
    def get(self):
        return "Error: Method not allowed"
    
    def post(self):
        args = self.parser.parse_args()
        email = args["email"]
        password = args["password"]

        # Add your login logic here

        user = users.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            return "incorrect credentials"

        login_user(user)

        return "login successful"

api.add_resource(loginApi, '/api/login')
api.add_resource(indexApi, '/api')
