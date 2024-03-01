from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, decode_token, set_access_cookies, unset_jwt_cookies, create_refresh_token, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request, render_template
from webApp import api, jwt, db, mail, app, socketio
from jwt.exceptions import ExpiredSignatureError
from webApp.models import users, esp32, token
from flask_restful import Resource, reqparse
from webApp.globalVar import otpTimeout
from webApp.function import genOTP
from flask_mail import Message
import time, random

#pin variables
stato = "26" #stato == start stop

genOtpStartTime = 0

verifyEmailRoute = ['/api/status', '/api/status/', '/api/updatepin', '/api/updatepin/', '/api/logout', '/api/logout/']
trackLogin = ['/api/resetpass', '/api/resetpass/']

@jwt.unauthorized_loader
def handle_unauthorized(callback):
    return ({"error": "Missing Authorization Header"}), 401

@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return ({"message": "expired token"}), 401

@jwt.invalid_token_loader
def handle_invalid(error):
    return ({"message": "invalid token",
                    "error":error}), 401    

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):

    jti = jwt_payload["jti"]
    Token = token.query.filter_by(jti=jti).first()

    if Token:
        return token is not None

@app.before_request
def verifyEmailRequest():

    if request.path in verifyEmailRoute:

        identity = request.headers.get('Authorization')

        try:

            token = identity[len("Bearer "):]

        except:

            return ({"error":"no authorization header in request"}), 400

        decoded_token = decode_token(token)
        payload = decoded_token['sub']

        email = payload['email']
        logged_user = users.query.filter_by(email=email).first()

        if logged_user.verifiedEmail != "True":

            return ({"error":"email verification not completed"}), 403

@app.before_request
def verifyUserLogin():

    if request.path in trackLogin:

        if 'access_token_cookie' in request.cookies and request.method != "PUT":   

            return ({"Error": "User is logged in, use 'PUT' method."}), 401
        
        if 'access_token_cookie' not in request.cookies and request.method != "GET":

            return ({"Error": "User is logged out, use 'GET' method."}), 401
     
class refreshApi(Resource):
    @jwt_required(refresh=True)
    def post(self):

        refresh_token = get_jwt()["jti"]
        id = get_jwt_identity()
        claims = {"refresh_jti":refresh_token}
        access_token = create_access_token(identity=id, additional_claims=claims)

        return jsonify(access_token=access_token), 200

class pinStatusApi(Resource):
    @jwt_required()
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("pin", required=True)

    def post(self):

        args = self.parser.parse_args()
        pin = args["pin"]
        
        query = esp32.query.filter_by(pinName='OS').first()
        status = query.switchState

        if status == "0":

            return jsonify({"Alert":"Esp is offline. Current state unknown"}), 503

        if pin == stato:
            
            query = esp32.query.filter_by(esp32pin=stato).first()
            state = query.switchState

            return ({"motor state": state}), 200
        
        return ({"error":"invalid pin"}), 400
 
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

        if role == "user":
        
            return ({"error":"not authorized"}), 401
        
        args = self.parser.parse_args()
        pnon = args["pin"]
        newState = args["state"]

        query = esp32.query.filter_by(pinName=pnon).first()

        if not query:

            query = esp32.query.filter_by(esp32pin=pnon).first()

            if not query:

                return ({"error":"invalid pin name or number"}), 400
        
        if newState != "1" and newState != "0":

            return ({"error":"invalid update value"}), 400
        
        onlineState = esp32.query.filter_by(pinName='OS').first()
        status = onlineState.switchState

        if status == "0":
            
            socketio.emit("offline", {"Alert":"Esp is offline. Current state unknown"})

            return ({"Alert":"Esp is offline. Current state unknown"}), 503
        
        query.switchState = newState

        try:

            db.session.commit()

            socketio.emit("webUpdate", {"stateUpdated": newState})

            return ({"success": "pin updated successfully"}),200
        
        except Exception as e:

            db.session.rollback()
            error_message = str(e) 

            return ({"error": "Failed to update pin", "Details": str(e)}), 500 
        
        finally:

            db.session.close()        

class queryApi(Resource):
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("pin", required=True)
        
    def post(self):

        args = self.parser.parse_args()
        pin = args["pin"]

        query = esp32.query.filter_by(esp32pin=pin).first()

        if query:

            state = query.switchState

            return jsonify(success = state)
        
        return jsonify({"error": "invalid pin"}), 404

class synchardchangesApi(Resource):

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("status", required=True)
        self.parser.add_argument("pin", required=True)

    def put(self):

        args = self.parser.parse_args()
        status = args["status"]
        pin = args["pin"]

        query = esp32.query.filter_by(esp32pin=pin).first()

        if not query:

            return jsonify({"error":"invalid pin entered"}), 400
        
        state = query.switchState

        if state != status:

            query.switchState = status

        try:

            db.session.commit()

            socketio.emit("localUpdate", {"update":status})

            return jsonify(success = status)   
             
        except Exception as e:

            db.session.rollback()
            error_message = str(e) 

            return jsonify({"Error": "Could not synchronize changes", "Details": str(e)}), 500
        
        finally:

            db.session.close()

class syncEmergencyApi(Resource):

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("emergency", required=True)

    def put(self):

        args = self.parser.parse_args()
        emergency = args["emergency"]

        socketio.emit("emergency", {"emergency":emergency})

        return jsonify({"success":"broadcast successful"}), 200
        
class loginApi(Resource):

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("email", required=True)
        self.parser.add_argument("password", required=True)

    def post(self):

        args = self.parser.parse_args()
        email = args["email"].lower()
        password = args["password"]

        try:

            user = users.query.filter_by(email=email).first()
            
            if not user or not check_password_hash(user.password, password):
                return ({"error": "incorrect credentials"}), 400

            loggedUser = {"email":email, "username":user.username, "role":user.role, "verified":user.verifiedEmail}
            refresh_token = create_refresh_token(identity=loggedUser)
            access_token = create_access_token(identity=loggedUser, fresh=True, additional_claims={"refresh_jti": decode_token(refresh_token)["jti"]})

            if user.verifiedEmail != "True":

                return ({"error": "email verification not complete"}), 403
            
            response = jsonify(

                {
                    "success": "login successful",
                    "token":{
                        "access_token":access_token, "refresh_token":refresh_token
                    }
                }
                
            )

            set_access_cookies(response, access_token)
            
            return response
        
        except Exception as e:

            db.session.rollback()
            error_message = str(e) 

            return ({"error": "could not login", "details": str(e)}),500
        
        finally:

            db.session.close()

class registerApi(Resource):

    # global genOtpStartTime
    # removed jsonify from all response in this route as it leads to server error

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("email", required=True)
        self.parser.add_argument("username", required=True)
        self.parser.add_argument("password", required=True)

    def post(self):

        args = self.parser.parse_args()
        email = args["email"].lower()
        username = args["username"].lower()
        password = args["password"]

        existingUserName = users.query.filter_by(username=username).first()
        existingMail = users.query.filter_by(email=email).first()

        if existingUserName:
            return ({"error": "username is already taken"}), 400
        
        if existingMail:
            return ({"error": "email already exist"}), 400

        otp, otpStartTime = genOTP()

        global genOtpStartTime 

        genOtpStartTime = otpStartTime

        msg = Message('Email Verification', recipients=[email])
        msg.html = render_template("emailVerification.html", otp=otp)

        try:

            mail.send(msg)

        except:

            return ({"error": "invalid email format"}), 400
        
        new_user = users(email=email, username=username, role="user", password=generate_password_hash(password), otp=otp)
        
        try:

            db.session.add(new_user)
            db.session.commit()

            return ({

                "success": "new user created and otp sent to mail",
                "email": email

            }), 200
        
        except Exception as e:

            db.session.rollback()
            error_message = str(e) 

            return ({"error": "failed to create user", "details": str(e)}), 500 
        
        finally:

            db.session.close()

class verifyEmailApi(Resource):

   # removed jsonify

    def __init__(self):

        self.parser = reqparse.RequestParser()

    def post(self):

        self.parser.add_argument("otp", required=True)
        self.parser.add_argument("email", required=True)

        global genOtpStartTime

        args = self.parser.parse_args()
        user_otp = args["otp"]
        email = args["email"].lower()

        logged_user = users.query.filter_by(email=email).first()

        if not logged_user:

            return ({"error": "email does not exist"}), 400

        if logged_user.verifiedEmail == "True":

            return ({"alert":"email verification already completed"}), 409

        if logged_user.otp != user_otp:

            return ({"error": "invalid otp entered"}), 400
        
        currentTime = time.time()

        if (currentTime - genOtpStartTime) > otpTimeout:

            logged_user.otp = " "

            try:

                db.session.commit()

                return ({"error": "expired otp, request for a new one"}), 400
            
            except Exception as e:

                db.session.rollback()
                error_message = str(e) 

                return ({"error": "failed to update db", "details": str(e)}), 500 
        
            finally:

                db.session.close()
        
        
        logged_user.otp = " "
        
        logged_user.verifiedEmail = "True"

        try:

            db.session.commit()

            return ({"success": "email verified successfully"}), 200
        
        except Exception as e:

            db.session.rollback()
            error_message = str(e) 

            return ({"error": "verification unsuccessfull", "Details": str(e)}), 500 
        
        finally:

            db.session.close()
    
    def put(self):

        self.parser.add_argument("email", required=True)
        self.parser.add_argument("newEmail", required=True)

        global genOtpStartTime

        args = self.parser.parse_args()
        updatedEmail = args["newEmail"].lower()
        email = args["email"].lower()


        logged_user = users.query.filter_by(email=email).first()
        confirmUpdatedEmail = users.query.filter_by(email=updatedEmail).first()

        if confirmUpdatedEmail:

            return ({"error": "email already exist, login instead"}), 409
        
        if logged_user:

            otp, otpStartTime = genOTP()

            genOtpStartTime = otpStartTime

            msg = Message('Email Verification', recipients=[updatedEmail])
            msg.html = render_template("emailVerification.html", otp=otp)

            try:

                mail.send(msg)

            except:

                return ({"Error": "Invalid email format"}), 400

            logged_user.otp = otp
            logged_user.email = updatedEmail

            try:

                db.session.commit()
                    
                return ({

                    "success": "email update completed and otp sent to new email",
                    "email": updatedEmail

                }), 200
            
            except Exception as e:

                db.session.rollback()
                error_message = str(e) 

                return ({"error": "update unsuccessfull", "details": str(e)}), 500 
        
            finally:

                db.session.close()
                    
        return ({"error":"invalid old email"}), 400       

    def get(self):

        self.parser.add_argument("email", required=True)

        try:
            
            global genOtpStartTime
            args = self.parser.parse_args()

            email = args["email"].lower()
            
            logged_user = users.query.filter_by(email=email).first()

            if logged_user.verifiedEmail == "True":

                return ({"alert":"email verification already completed"}), 409
            
            otp, otpStartTime = genOTP()

            genOtpStartTime = otpStartTime

            msg = Message('Industrial IOT email Verification', recipients=[email])
            msg.html = render_template("emailVerification.html", otp=otp)
            
            try:

                mail.send(msg)

            except:

                return ({"error": "invalid email format"}), 400

            logged_user.otp = otp

            try:
                db.session.commit()

                return ({"success": "otp sent to mail"}), 200
            
            except Exception as e:

                db.session.rollback()
                error_message = str(e) 

                return ({"error": "could not update db", "details": str(e)}), 500 
        
            finally:

                db.session.close()
        
        except Exception as e:

            error_message = str(e) 

            return ({"error": "OTP generation failed", "details": str(e)}), 500
    
class genOtpApi(Resource):
    @jwt_required()
    def get(self):

        try:
            global genOtpStartTime

            user = get_jwt_identity()
            email = user["email"]
            
            logged_user = users.query.filter_by(email=email).first()

            if logged_user.verifiedEmail == "True":

                return {"Msg":"email verification already completed"}
            
            otp, otpStartTime = genOTP()

            genOtpStartTime = otpStartTime

            msg = Message('Industrial IOT email Verification', recipients=[email])
            msg.html = render_template("emailVerification.html", otp=otp)
            
            try:

                mail.send(msg)

            except:

                return ({"Error": "Invalid email format"}), 400

            logged_user.otp = otp

            try:
                db.session.commit()

                return ({"status": "otp sent to mail"})
            
            except Exception as e:

                db.session.rollback()
                error_message = str(e) 

                return ({"Error": "could not send to mail", "Details": str(e)}), 500 
        
            finally:

                db.session.close()
        
        except:

            return ({"error": "login before requesting otp"}), 400

class resetPasswordApi(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()

    def get(self):
        
        self.parser.add_argument("email", required=True)
        args = self.parser.parse_args()
        email = args["email"].lower()

        logged_user = users.query.filter_by(email=email).first()

        if not logged_user:

            return ({"error":"incorrect email"}), 400
        
        global genOtpStartTime

        otp, otpStartTime = genOTP()

        genOtpStartTime = otpStartTime

        token = str(otp)+logged_user.username

        logged_user.token = token

        try:

            db.session.commit()

            msg = Message('Password reset', recipients=[email])
            msg.html = render_template("apiResetToken.html", token=token, username=logged_user.username)

            try:

                mail.send(msg)

            except:

                return ({"error": "invalid email format"}), 400

            return ({"success": "token sent to email"}), 200
        
        except Exception as e:

            db.session.rollback()
            error_message = str(e) 

            return ({"error": "failed to store token", "details": str(e)}), 500 
        
        finally:

            db.session.close()

    @jwt_required()
    def put(self):

        self.parser.add_argument("oldpass", required=True)
        self.parser.add_argument("newpass", required=True)
        args = self.parser.parse_args()
        oldPass = args["oldpass"]
        newPass = args["newpass"]

        user = get_jwt_identity()
        email = user["email"]

        logged_user = users.query.filter_by(email=email).first()

        if not check_password_hash(logged_user.password, oldPass):

            return ({"error":"incorrect old password, logout to reset password or try again"}), 400
        
        logged_user.password = generate_password_hash(newPass)

        try:

            db.session.commit()
        
        except Exception as e:

            db.session.rollback()
            error_message = str(e) 

            return ({"error": "failed to update password", "details": str(e)}), 500 
        
        finally:

            db.session.close()

        return ({"success": "password updated successfully"}), 200
    
class resetOutTokenApi(Resource):

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("token", required=True)
        self.parser.add_argument("new", required=True)

    def put(self):

        if 'access_token_cookie' in request.cookies:   

            return jsonify({"error": "user is logged in"}), 401
        
        args = self.parser.parse_args()
        token = args["token"]
        newPass = args["new"]

        # otp = token.split(token[6:])[0]
        username = token.split(token[0:6])[1]

        global genOtpStartTime

        verifyUser = users.query.filter_by(username=username).first()

        if not verifyUser:
                
            return jsonify({"error":"invalid token"}), 400
        
        if verifyUser.token != token:

            return jsonify({"error":"invalid token"}), 400
            
        currentTime = time.time()

        if (currentTime - genOtpStartTime) > otpTimeout:

            verifyUser.otp = " "

            try:

                db.session.commit()

                return jsonify({"error": "expired token"}),400
            
            except Exception as e:

                db.session.rollback()
                error_message = str(e) 

                return jsonify({"error": "failed to trash expired token", "details": str(e)}), 500 
        
            finally:

                db.session.close()
                             
        
        verifyUser.password = generate_password_hash(newPass)
        verifyUser.token = " "

        try:

            db.session.commit()

            return jsonify({"success":"password updated successfully"}), 200
        
        except Exception as e:

            db.session.rollback()
            error_message = str(e) 

            return jsonify({"error": "password update unsuccessfull", "details": str(e)}), 500 
        
        finally:

            db.session.close()
    
class logOutApi(Resource):
    @jwt_required()
    def post(self):

        jti = get_jwt()["jti"]
        response = jsonify({"success": "logout successful"})

        unset_jwt_cookies(response)

        db.session.add(token(jti=jti))

        refresh_jti = get_jwt()["refresh_jti"]

        db.session.add(token(jti=refresh_jti))

        try:

            db.session.commit()

            return response
        
        except Exception as e:

            db.session.rollback()
            error_message = str(e) 

            return jsonify({"error": "logout unsuccesful", "details": str(e)}), 500 
        
        finally:

            db.session.close()

class updateRoleApi(Resource):
    @jwt_required()
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("email", required=True)
        self.parser.add_argument("role", required=True)

    def put(self):

        args = self.parser.parse_args()
        userEmail = args["email"].lower()
        newRole = args["role"].lower()

        user = get_jwt_identity()
        email = user["email"]
        role = user["role"]        
        
        if role != "owner":

            return ({"Error":"not authorized"}), 401
        
        update_user = users.query.filter_by(email=userEmail).first()

        if not update_user:

            return ({"Error": "Invalid Email"}), 400
        
        if update_user.verifiedEmail != "True":

            return ({"Error": "User has not verified thier email"}), 400
        
        if newRole != "user" and newRole != "admin":

            return ({"Error": "Unknown role"}), 400
        
        if update_user.role == newRole:

            return ({"Msg": "Role not updated but same"}), 304
        
        update_user.role = newRole

        try:
            db.session.commit()

            return ({"success": userEmail + " role, has been updated successfully"})
        
        except Exception as e:

            db.session.rollback()
            error_message = str(e) 

            return jsonify({"Error": "Failed to update user", "Details": str(e)}), 500 
        
        finally:

            db.session.close()

class deleteApi(Resource):
    @jwt_required()
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("email", required=True)

    def delete(self):

        args = self.parser.parse_args()
        userEmail = args["email"].lower()

        user = get_jwt_identity()
        role = user["role"]
        email = user["email"]
        
        if role != "owner":

            return ({"Error":"not authorized"}), 401
        
        if userEmail == email:

            return ({"Error":"owner cannot be deleted"}), 401
        
        del_user = users.query.filter_by(email=userEmail).first()

        if not del_user:

            return ({"Error": "Invalid Email"})
        
        try:
            db.session.delete(del_user)
            db.session.commit()

            return ({"success": userEmail + " has been deleted from the database"})
        
        except Exception as e:

            db.session.rollback()
            error_message = str(e) 

            return jsonify({"Error": "Failed to delete user", "Details": str(e)}), 500 
        
        finally:

            db.session.close()

class usersApi(Resource):
    @jwt_required()
    def get(self):
        

        user = get_jwt_identity()
        role = user["role"]
        email = user["email"]
            
        if role != "owner":

            return ({"Error":"not authorized"}), 401
        
        regUser = users.query.with_entities(users.id, users.username, users.email, users.role, users.verifiedEmail).all()

        serialized_users = []

        for row in regUser:

            user_dict = {

                "id": row.id,
                "username": row.username,
                "email": row.email,
                "role": row.role,
                "verified Email": row.verifiedEmail
                    
            }

            serialized_users.append(user_dict)

        return jsonify(registeredUsers=serialized_users)

api.add_resource(queryApi, '/api/query', '/api/query/')
api.add_resource(loginApi, '/api/login', '/api/login/')
api.add_resource(usersApi, '/api/users', '/api/users/')
api.add_resource(deleteApi, '/api/delete', '/api/delete/')
api.add_resource(logOutApi, '/api/logout', '/api/logout/')
# api.add_resource(genOtpApi, '/api/genotp', '/api/genotp/')
api.add_resource(pinStatusApi, '/api/status', '/api/status/')
api.add_resource(registerApi, '/api/register', '/api/register/')
api.add_resource(refreshApi, '/api/refreshjwt', '/api/refreshjwt/')
api.add_resource(updatePinApi, '/api/updatepin', '/api/updatepin/')
api.add_resource(updateRoleApi, '/api/updaterole', '/api/updaterole/')
api.add_resource(syncEmergencyApi, '/api/emergency', '/api/emergency/')
api.add_resource(resetPasswordApi, '/api/resetpass', '/api/resetpass/')
api.add_resource(verifyEmailApi, '/api/verifyemail', '/api/verifyemail/')
api.add_resource(resetOutTokenApi, '/api/resetouttoken', '/api/resetouttoken/')
api.add_resource(synchardchangesApi, '/api/synchardchanges', '/api/synchardchanges/')
