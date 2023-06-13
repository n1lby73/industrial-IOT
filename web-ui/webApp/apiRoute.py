from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource, reqparse
from webApp.models import users, esp32
from webApp import api, jwt
from flask import jsonify

class indexApi(Resource):
    @jwt_required()
    def get(self):
        query = esp32.query.filter_by(esp32pin='5').first()
        state = query.switchState
        return ({"motor state": state}), 200

class loginApi(Resource):

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("email", required=True)
        self.parser.add_argument("password", required=True)
    
    def get(self):

        return ({"msg": "Method not allowed"}), 405
    
    def post(self):

        args = self.parser.parse_args()
        email = args["email"]
        password = args["password"]

        user = users.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            return ({"msg": "incorrect credentials"}), 401

        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token)

api.add_resource(loginApi, '/api/login')
api.add_resource(indexApi, '/api')
