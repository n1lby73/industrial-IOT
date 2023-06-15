from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource, reqparse
from webApp.models import users, esp32
from webApp import api, jwt, db
from flask import jsonify

#pin variables
stato = "5" #stato == start stop

class indexApi(Resource):
    @jwt_required()
    def get(self, pinStatus):

        if pinStatus == stato:
            
            query = esp32.query.filter_by(esp32pin=stato).first()
            state = query.switchState

            return ({"motor state": state}), 200
        
        return ({"error":"invalid pin"})

# pnon ==> pin name or number
class updateApi(Resource):
    @jwt_required()
    def put(self, pnon, newState):
        
        user = get_jwt_identity()
        role = user["role"]

        if role == "user":
            return {"error":"not authorized"}

        try:

            query = esp32.query.filter_by(pinName=pnon).first()

        except AttributeError:

            query = esp32.query.filter_by(esp32pin=pnon).first()

        else:
            return {"error":"invalid pin name or number"}
        
        if newState != "1" and newState != "0":
            return {"error":"invalid update msg"}
        
        query = esp32.query.filter_by(pinName='onlineStatus').first()
        status = query.switchState

        if status == "0":
            return {"Alert":"Esp is offline, can't update"}
        
        try:

            query = esp32.query.filter_by(pinName=pnon).first()
            query.switchState = newState
            db.session.commit()

        except:

            query = esp32.query.filter_by(esp32pin=pnon).first()
            query.switchState = newState
            db.session.commit()

        return ({"status":"success"}), 200

class loginApi(Resource):

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("email", required=True)
        self.parser.add_argument("password", required=True)

    def post(self):

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

    def post(self):

        args = self.parser.parse_args()
        email = args["email"]
        username = args["username"]
        password = args["password"]

        existingUserName = users.query.filter_by(username=username).first()
        existingMail = users.query.filter_by(email=email).first()

        if existingUserName:
            return ({"Error": "Username is already taken"})
        
        if existingMail:
            return ({"Error": "Email already exit"})

        new_user = users(email=email, username=username, role="user", password=generate_password_hash(password))

        db.session.add(new_user)
        db.session.commit()

        return ({"Sucess": "new user created"})

api.add_resource(loginApi, '/api/login')
api.add_resource(registerApi, '/api/register')
api.add_resource(indexApi, '/api/<pinStatus>')
api.add_resource(updateApi, '/api/update/<pnon>/<newState>')
