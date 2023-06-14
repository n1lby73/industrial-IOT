from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource, reqparse
from webApp.models import users, esp32
from webApp import api, jwt, db
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

        # if get_jwt_identity():
        #     return ({"msg: A user is already logged in"})
        
        args = self.parser.parse_args()
        email = args["email"]
        password = args["password"]

        user = users.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            return ({"msg": "incorrect credentials"})

        loggedUser = {"email":email, "username":user.username, "role":user.role}
        access_token = create_access_token(identity=loggedUser)
        return jsonify(access_token=access_token)

class registerApi(Resource):

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("email", required=True)
        self.parser.add_argument("username", required=True)
        self.parser.add_argument("password", required=True)
        self.parser.add_argument("confirmPassword", required=True)
    
    def get(self):

        return ({"msg": "Method not allowed"}), 405
    
    def post(self):

        args = self.parser.parse_args()
        email = args["email"]
        username = args["username"]
        password = args["password"]
        password2 = args["confirmPassword"]

        existingUserName = users.query.filter_by(username=username).first()
        existingMail = users.query.filter_by(email=email.data).first()

        if existingUserName:
            return {"Error: Username is already taken"}
        
        if existingMail:
            return {"Error: Email already exit"}
        
        if password != password2:
            return {"error: password do not match"}
        
        new_user = users(email=email, username=username, role="user", password=generate_password_hash(password))

        db.session.add(new_user)
        db.session.commit()

        return {"Sucess: new user created"}
    
api.add_resource(indexApi, '/api')
api.add_resource(loginApi, '/api/login')
api.add_resource(registerApi, '/api/register')

