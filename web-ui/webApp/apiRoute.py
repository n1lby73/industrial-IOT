from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, decode_token, jwt_manager, set_access_cookies, unset_access_cookies
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request, render_template, session
from jwt.exceptions import ExpiredSignatureError
from flask_restful import Resource, reqparse
from webApp import api, jwt, db, cache, mail
from webApp.globalVar import otpTimeout
from webApp.models import users, esp32
from webApp.function import genOTP
from datetime import timedelta
from flask_mail import Message
import time, random

#pin variables
stato = "5" #stato == start stop

genOtpStartTime = 0

class pinStatusApi(Resource):
    @jwt_required()
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("pin", required=True)

    def get(self):

        user = get_jwt_identity()
        email = user["email"]
        
        args = self.parser.parse_args()
        status = args["pin"]

        if not session.get(email):

            return ({"Error":"User not logged in"})

        logged_user = users.query.filter_by(email=email).first()

        if logged_user.verifiedEmail != "True":

            return {"error":"email verification not completed"}
        
        query = esp32.query.filter_by(pinName='onlineStatus').first()
        status = query.switchState

        if status == "0":

            return {"Alert":"Esp is offline. Current state unknown"}

        if status == stato:
            
            query = esp32.query.filter_by(esp32pin=stato).first()
            state = query.switchState

            return ({"motor state": state}), 200
        
        return ({"error":"invalid pin"})

# pnon ==> pin name or number
class updatePinApi(Resource):
    @jwt_required()
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("pin", required=True)
        self.parser.add_argument("state", required=True)

    def put(self):
        
        user = get_jwt_identity()
        role = user["role"]
        email = user["email"]

        if not session.get(email):

            return ({"Error":"User not logged in"})

        logged_user = users.query.filter_by(email=email).first()

        if logged_user.verifiedEmail != "True":

            return {"error":"email verification not completed"}

        if role == "user":
            return {"error":"not authorized"}
        
        args = self.parser.parse_args()
        pnon = args["pin"]
        newState = args["state"]

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

        try:

            user = users.query.filter_by(email=email).first()
            
            if not user or not check_password_hash(user.password, password):
                return ({"msg": "incorrect credentials"})

            loggedUser = {"email":email, "username":user.username, "role":user.role}
            access_token = create_access_token(identity=loggedUser)

            # cache.set(email, access_token)
            # session[email] = access_token
            response = jsonify({"msg": "login successful"}, {"token":access_token})

            set_access_cookies(response, access_token)
            
            return response
        
        except Exception as e:

            db.session.rollback()
            error_message = str(e) 

            return jsonify({"Error": "Could not login", "Details": str(e)}), 500 

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

        try:

            mail.send(msg)

        except:

            return ({"Error": "Invalid email format"})
        
        new_user = users(email=email, username=username, role="user", password=generate_password_hash(password), otp=otp)
        
        try:

            db.session.add(new_user)
            db.session.commit()

            return ({"Sucess": "new user created and otp sent to mail"})
        
        except Exception as e:

            db.session.rollback()
            error_message = str(e) 

            return jsonify({"Error": "Failed to create user", "Details": str(e)}), 500 
        
        finally:

            db.session.close()

class verifyEmailApi(Resource):
    @jwt_required()
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("otp", required=True)

    def put(self):

        global genOtpStartTime
        try:

            user = get_jwt_identity()
            email = user["email"]
        
        except ExpiredSignatureError:

            # Handle the expired token error
            return jsonify({"error": "Token has expired. Please re-authenticate."}), 401
        
        except:
            
            return jsonify({"error": "Invalid token."}), 401

        if not session.get(email):

            return ({"Error":"User not logged in"})

        logged_user = users.query.filter_by(email=email).first()

        if logged_user.verifiedEmail == "True":

            return {"Msg":"email verification already completed"}

        args = self.parser.parse_args()
        user_otp = args["otp"]

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
        try:
            global genOtpStartTime

            user = get_jwt_identity()
            email = user["email"]

            if not session.get(email):

                return ({"Error":"User not logged in"})
            
            logged_user = users.query.filter_by(email=email).first()

            if logged_user.verifiedEmail == "True":

                return {"Msg":"email verification already completed"}
            
            otp, otpStartTime = genOTP()

            genOtpStartTime = otpStartTime

            msg = Message('Api email Verification', recipients=[email])
            msg.html = render_template("emailVerification.html", otp=otp)
            
            try:

                mail.send(msg)

            except:

                return ({"Error": "Invalid email format"})

            logged_user.otp = otp

            db.session.commit()

            return ({"status": "otp sent to mail"})
        
        except:

            return ({"error": "login before requesting otp"})

# class resetPassApi(Resource):
#     @jwt_required(optional=True)
#     def __init__(self):

#         self.parser = reqparse.RequestParser()
#         self.parser.add_argument("oldpass", required=True)
#         self.parser.add_argument("newpass", required=True)
#         self.parser.add_argument("email", required=True)

#     def put(self):

#         args = self.parser.parse_args()
#         emailLoggedOut = args["email"]
#         oldPass = args["oldpass"]
#         newPass = args["newpass"]
        
#         if get_jwt_identity() is None and emailLoggedOut is None:

#             return {"error": "User is logged out, provide email parameter only"}, 400
        
#         if get_jwt_identity() is None and emailLoggedOut is not None:

#             # if session.get(email):

#             # return ({"Error": "User is already logged in. Please use a different route."})

#             logged_user = users.query.filter_by(email=emailLoggedOut).first()

#             if not logged_user:

#                 return ({"Error":"Incorrect email"})
            
#             loggedUser = {"email":emailLoggedOut, "username":logged_user.username, "role":logged_user.role}
#             access_token = create_access_token(identity=loggedUser, expires_delta=timedelta(seconds=300))

#             logged_user.token = access_token

#             db.session.commit()

#             msg = Message('Api Password reset', recipients=[email])
#             msg.html = render_template("apiResetToken.html", token=access_token, username=logged_user.username)

#             try:

#                 mail.send(msg)

#             except:

#                 return ({"Error": "Invalid email format"})

#             return ({"Msg": "Token sent to email"}), 200
        
#         user = get_jwt_identity()
#         email = user["email"]

#         if not session.get(email):

#             return ({"Error":"User not logged in"})

#         logged_user = users.query.filter_by(email=email).first()

#         if not check_password_hash(logged_user.password, oldPass):

#             return ({"Error":"Incorrect old password, logout to reset password or try again"})
        
#         logged_user.password = generate_password_hash(newPass)
#         db.session.commit()

#         return ({"Msg": "Password updated successfully"})

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

        if not session.get(email):

            return ({"Error":"User not logged in"})

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

        if session.get(email):

            return ({"Error": "User is already logged in. Please use a different route."})

        logged_user = users.query.filter_by(email=email).first()

        if not logged_user:

            return ({"Error":"Incorrect email"})
        
        loggedUser = {"email":email, "username":logged_user.username, "role":logged_user.role}
        access_token = create_access_token(identity=loggedUser, expires_delta=timedelta(seconds=120))

        logged_user.token = access_token

        db.session.commit()

        msg = Message('Api Password reset', recipients=[email])
        msg.html = render_template("apiResetToken.html", token=access_token, username=logged_user.username)

        try:

            mail.send(msg)

        except:

            return ({"Error": "Invalid email format"})

        return ({"Msg": "Token sent to email"})
    
class resetOutTokenApi(Resource):

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("token", required=True)
        self.parser.add_argument("new", required=True)

    def put(self, token, newPass):

        args = self.parser.parse_args()
        user_token = args["token"]
        newPass = args["new"]

        try:

            decoded_token = decode_token(user_token)

            payload = decoded_token['sub']

            email = payload['email']

            verifyEmail = users.query.filter_by(email=email).first()

            if verifyEmail.token != user_token:
                
                return ({"Error":"Invalid Token"})
                             
        except:

            return ({"Error":"Expired token"})
        
        verifyEmail.password = generate_password_hash(newPass)
        verifyEmail.token = " "

        db.session.commit()

        return ({"Success":"Password updated successfully"})
    
class logOutApi(Resource):
    @jwt_required()
    def post(self):

        # cache.clear()
        session.clear()

        return ({"Msg":"Logged out successfully"})

class updateRoleApi(Resource):
    @jwt_required()
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("email", required=True)
        self.parser.add_argument("role", required=True)

    def put(self):

        args = self.parser.parse_args()
        userEmail = args["email"]
        newRole = args["role"]

        user = get_jwt_identity()
        email = user["email"]
        role = user["role"]

        if not session.get(email):

            return ({"Error":"User not logged in"})
        
        
        if role != "owner":

            return ({"Error":"not authorized"})
        
        update_user = users.query.filter_by(email=userEmail).first()

        if not update_user:

            return ({"Error": "Invalid Email"})
        
        if update_user.verifiedEmail != "True":

            return ({"Error": "User has not verified thier email"})
        
        if newRole != "user" and newRole != "admin":

            return ({"Error": "Unknown role"})
        
        if update_user.role == newRole:

            return ({"Msg": "Role not updated but same"})
        
        update_user.role = newRole
        db.session.commit()

        return ({"Msg": userEmail + " role, has been updated successfully"})

class deleteApi(Resource):
    @jwt_required()
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("email", required=True)

    def delete(self):

        args = self.parser.parse_args()
        userEmail = args["email"]

        user = get_jwt_identity()
        role = user["role"]
        email = user["email"]

        if not session.get(email):

            return ({"Error":"User not logged in"})
        
        if role != "owner":

            return ({"Error":"not authorized"})
        
        del_user = users.query.filter_by(email=userEmail).first()

        if not del_user:

            return ({"Error": "Invalid Email"})
        
        db.session.delete(del_user)
        db.session.commit()

        return ({"Msg": userEmail + " has been deleted from the database"})

class usersApi(Resource):
    @jwt_required()
    def get(self):
        
        user = get_jwt_identity()
        role = user["role"]
        email = user["email"]

        if not session.get(email):

            return ({"Error":"User not logged in"})
        
        if role != "owner":

            return ({"Error":"not authorized"})
    
        regUser = users.query.with_entities(users.id, users.username, users.email, users.role).all()

        serialized_users = []

        for row in regUser:

            user_dict = {

                "id": row.id,
                "username": row.username,
                "email": row.email,
                "role": row.role
                
            }

            serialized_users.append(user_dict)

        return jsonify(registeredUsers=serialized_users)

api.add_resource(loginApi, '/api/login', '/api/login/')
api.add_resource(usersApi, '/api/users', '/api/users/')
api.add_resource(deleteApi, '/api/delete', '/api/delete/')
api.add_resource(logOutApi, '/api/logout', '/api/logout/')
api.add_resource(genOtpApi, '/api/genotp', '/api/genotp/')
api.add_resource(resetInApi, '/api/resetin', '/api/resetin/')
api.add_resource(pinStatusApi, '/api/status', '/api/status/')
api.add_resource(resetOutApi, '/api/resetout', '/api/resetout/')
api.add_resource(registerApi, '/api/register', '/api/register/')
api.add_resource(updatePinApi, '/api/updatepin', '/api/updatepin/')
api.add_resource(updateRoleApi, '/api/updaterole', '/api/updaterole/')
api.add_resource(verifyEmailApi, '/api/verifyemail', '/api/verifyemail/')
api.add_resource(resetOutTokenApi, '/api/resetouttoken', '/api/resetouttoken/')
