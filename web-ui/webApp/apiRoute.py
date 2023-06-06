from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from webApp.models import users, esp32
from webApp import api

class indexApi(Resource):
    @jwt_required()
    def get(self):
        return "users are  authorized"

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

        return "login successful"

api.add_resource(loginApi, '/api/login')
api.add_resource(indexApi, '/api')
