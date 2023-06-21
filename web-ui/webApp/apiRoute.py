from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, decode_token, jwt_manager
from werkzeug.security import generate_password_hash, check_password_hash
from webApp import mail
from flask_mail import Message
from webApp.globalVar import otpTimeout
from webApp.function import genOTP
from flask_restful import Resource, reqparse
from webApp.models import users, esp32
from webApp import api, jwt, db
from flask import jsonify, request, render_template
from datetime import timedelta
import time, random

#pin variables
stato = "5" #stato == start stop

genOtpStartTime = 0

class indexApi(Resource):
    @jwt_required()
    def get(self, pinStatus):

        user = get_jwt_identity()
        email = user["email"]

        logged_user = users.query.filter_by(email=email).first()

        if logged_user.verifiedEmail != "True":

            return {"error":"email verification not completed"}

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
        email = user["email"]

        logged_user = users.query.filter_by(email=email).first()

        if logged_user.verifiedEmail != "True":

            return {"error":"email verification not completed"}

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

    global genOtpStartTime

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

        otp, otpStartTime = genOTP()

        genOtpStartTime = otpStartTime

        msg = Message('Api email Verification', recipients=[email])
        msg.html = render_template("emailVerification.html", otp=otp)
        mail.send(msg)

        new_user = users(email=email, username=username, role="user", password=generate_password_hash(password), otp=otp)

        db.session.add(new_user)
        db.session.commit()

        return ({"Sucess": "new user created and otp sent to mail"})

class verifyEmailApi(Resource):
    @jwt_required()
    def put(self, user_otp):

        global genOtpStartTime
        
        user = get_jwt_identity()
        email = user["email"]

        logged_user = users.query.filter_by(email=email).first()

        if logged_user.verifiedEmail == "True":

            return {"Msg":"email verification already completed"}

        if logged_user.otp != user_otp:

            return ({"Error": "Invalid otp entered"})
        
        currentTime = time.time()

        if (currentTime - genOtpStartTime) > otpTimeout:

            logged_user.otp = " "
            db.session.commit()

            return ({"error": "Expired otp, request for a new one"})
        
        logged_user.otp = " "
        logged_user.verifiedEmail = "True"

        db.session.commit()

        return ({"Success": "Email verified successfully"})

class genOtpApi(Resource):
    @jwt_required()
    def get(self):

        global genOtpStartTime

        user = get_jwt_identity()
        email = user["email"]

        logged_user = users.query.filter_by(email=email).first()

        if logged_user.verifiedEmail == "True":

            return {"Msg":"email verification already completed"}
        
        otp, otpStartTime = genOTP()

        genOtpStartTime = otpStartTime

        msg = Message('Api email Verification', recipients=[email])
        msg.html = render_template("emailVerification.html", otp=otp)
        mail.send(msg)

        logged_user.otp = otp

        db.session.commit()

        return ({"status": "otp sent to mail"})
        
class resetInApi(Resource):
    @jwt_required()
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("oldpass", required=True)
        self.parser.add_argument("newpass", required=True)

    def put(self):

        args = self.parser.parse_args()
        oldPass = args["oldpass"]
        newPass = args["newpass"]

        user = get_jwt_identity()
        email = user["email"]

        logged_user = users.query.filter_by(email=email).first()

        if not check_password_hash(logged_user.password, oldPass):

            return ({"Error":"Incorrect old password, logout to reset password or try again"})
        
        logged_user.password = generate_password_hash(newPass)
        db.session.commit()

        return ({"Msg": "Password updated successfully"})

class resetOutApi(Resource):

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("email", required=True)

    def get(self):
        
        args = self.parser.parse_args()
        email = args["email"]

        logged_user = users.query.filter_by(email=email).first()

        if not logged_user:

            return ({"Error":"Incorrect email"})
        
        loggedUser = {"email":email, "username":logged_user.username, "role":logged_user.role}
        access_token = create_access_token(identity=loggedUser, expires_delta=timedelta(seconds=120))

        logged_user.token = access_token

        db.session.commit()

        msg = Message('Api Password reset', recipients=[email])
        msg.html = render_template("apiResetToken.html", token=access_token, username=logged_user.username)
        mail.send(msg)

        return ({"Msg": "Token sent to email"})
    
class resetOutTokenApi(Resource):

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("token", required=True)

    def put(self, token, newPass):

        try:

            decoded_token = decode_token(token)

            payload = decoded_token['sub']

            email = payload['email']

            verifyEmail = users.query.filter_by(email=email).first()

            if verifyEmail.token != token:
                
                return ({"Error":"Invalid Token"})
                             
        except:

            return ({"Error":"Expired token"})
        
        verifyEmail.password = generate_password_hash(newPass)
        verifyEmail.token = " "

        db.session.commit()

        return ({"Success":"Password updated successfully"})
    
api.add_resource(loginApi, '/api/login', '/api/login/')
api.add_resource(genOtpApi, '/api/genotp', '/api/genotp/')
api.add_resource(resetInApi, '/api/resetin', '/api/resetin/')
api.add_resource(resetOutApi, '/api/resetout', '/api/resetout/')
api.add_resource(registerApi, '/api/register', '/api/register/')
api.add_resource(indexApi, '/api/<pinStatus>', '/api/<pinStatus>/')
api.add_resource(updateApi, '/api/update/<pnon>/<newState>', '/api/update/<pnon>/<newState>/')
api.add_resource(verifyEmailApi, '/api/verifyemail/<user_otp>', '/api/verifyemail/<user_otp>/')
api.add_resource(resetOutTokenApi, '/api/resetouttoken/<token>/<newPass>', '/api/resetouttoken/<token>/<newPass>/')
