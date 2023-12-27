from flask_jwt_extended import get_jwt_identity,verify_jwt_in_request
from webApp.models import token
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

# Emitting sockets locations are: 
# syncEmergencyApi with event emergency
# updatePinApi with event offline and webUpdate
# syncHardChanges with event localUpdate

@socketio.on('role')
def websocket(role=None):

    try:

        if role is None:

            raise TypeError("no data passed on emitting the role event")

        tokenValue = role['authorization']
            
        if tokenValue:

            decoded_token = jwt.decode(tokenValue, os.getenv("SECRET_KEY"), algorithms=['HS256'])

            isRevoked = check_if_token_revoked(tokenValue)

            if isRevoked:

                return ({"error":"revoked token"})

            roleDict = decoded_token["sub"]

            userRole = roleDict["role"]

            socketio.emit('roleProcessed',{"role":userRole}, room=request.sid)

            return ({"success":"role emitted successfully"}),200

        else:

            return ({"error":"invalid data structure passed"}), 400

    except jwt.ExpiredSignatureError:

        return ({"error":"Token has expired"}), 401

    except jwt.InvalidTokenError:

        return ({"error":"Invalid token"}), 401

    except TypeError as e:

        return (f"Error: {e}"), 400
