from flask_login import current_user, login_user, logout_user
from flask_restful import Resource, reqparse
from flask import request
from webApp import login
from webApp import api

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
        extra_params = set(request.json.keys()) - set(self.parser.args.keys())
        if extra_params:
            error_message = f"Unexpected parameters: {', '.join(extra_params)}"
            return {"error": error_message}, 400

        email = args["email"]
        password = args["password"]
        # Add your login logic here
        return "The login API was called"

api.add_resource(loginApi, '/api/login')
api.add_resource(indexApi, '/api')
