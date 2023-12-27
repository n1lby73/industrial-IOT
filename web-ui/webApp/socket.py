from flask_jwt_extended import get_jwt_identity,verify_jwt_in_request
from dotenv import load_dotenv
from webApp import socketio
from flask import request
import jwt, os

load_dotenv()

# Emitting sockets locations are: 
# syncEmergencyApi with event emergency
# updatePinApi with event offline and webUpdate
# syncHardChanges with event localUpdate

@socketio.on('role')
def websocket(role=None):

    try:

        if role is None:
            raise TypeError("Argument 'role' is missing")

        token = role.get('headers')
            
        if token:

            try:

                headers = token.get("Authorization")
                tokenValue = headers[len("Bearer "):]

                decoded_token = jwt.decode(tokenValue, os.getenv("SECRET_KEY"), algorithms=['HS256'])

                socketio.emit('storeRole',{"role":tokenValue}, room=request.sid)
            
            except jwt.ExpiredSignatureError:
        
                print("Token has expired")

            except jwt.InvalidTokenError:
        
                print("Invalid token")

            except:

                print("not valid")
        else:
            print(role)
            print ("no token")

    except TypeError as e:

        return (f"error: {e}"), 400
        print(f"error: {e}")
    
    # except jwt.ExpiredSignatureError:
        
    #     print("Token has expired.")

    # # except jwt.InvalidTokenError:
        
    # #     print("Invalid token.")
