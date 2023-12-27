from flask_jwt_extended import get_jwt_identity,verify_jwt_in_request
from webApp.models import token, esp32
from dotenv import load_dotenv
from webApp import socketio
from flask import request
import jwt, os

load_dotenv()

def check_if_token_revoked(jwtToken):

    decoded_token = jwt.decode(jwtToken, os.getenv("SECRET_KEY"), algorithms=['HS256'])

    jti = decoded_token["jti"]
    Token = token.query.filter_by(jti=jti).first()

    if Token:

        return True

def socket_authorization_and_emitter(listenHandler, data, room):

    try:

        if data is None:

            raise TypeError(f"no data passed on emitting the {listenHandler} event")

        tokenValue = data['authorization']
            
        if tokenValue:

            decoded_token = jwt.decode(tokenValue, os.getenv("SECRET_KEY"), algorithms=['HS256'])

            isRevoked = check_if_token_revoked(tokenValue)

            if isRevoked:

                return ({"error":"revoked token"})

            if listenHandler == "role":

                roleDict = decoded_token["sub"]

                userRole = roleDict["role"]

                socketio.emit('roleProcessed',{"role":userRole}, room=room)

            elif listenHandler == "motorState":

                query = esp32.query.filter_by(esp32pin="26").first()
                state = query.switchState

                socketio.emit('motorStateProcessed',{"state":state}, room=room)

            return ({"success":f"{listenHandler} emitted successfully"}),200

        else:

            return ({"error":"invalid data structure passed"}), 400

    except jwt.ExpiredSignatureError:

        return ({"error":"Token has expired"}), 401

    except jwt.InvalidTokenError:

        return ({"error":"Invalid token"}), 401

    except TypeError as e:

        return (f"Error: {e}"), 400


# Emitting sockets locations are: 
# syncEmergencyApi with event emergency
# updatePinApi with event offline and webUpdate
# syncHardChanges with event localUpdate

@socketio.on('role')
def websocket(roleData=None):

    socket_authorization_and_emitter("role", roleData, request.sid)

@socketio.on('motorState')
def websocket(motorStateData=None):

    socket_authorization_and_emitter("motorState", motorStateData, request.sid)
