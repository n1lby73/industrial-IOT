from webApp.globalVar import espOnlineTimeout, espStartTime, espstate
from webApp import app, socketio
import random
import time


def confirmOnline():
    with app.app_context():

        global espOnlineTimeout, espStartTime, espstate

        currentTime = time.time()

        print("----------------------from function-------------------")
        print(espStartTime)
        
        if currentTime - espStartTime > espOnlineTimeout:

            espstate = 0
            socketio.emit('espOnlineState', {"value":0})
            # query = esp32.query.filter_by(pinName='onlineStatus').first()
            # query.switchState = str(espstate)
            # db.session.commit()
            # print("0")

        else:
            espstate = 1
            socketio.emit('espOnlineState', {"value":1})
            # query = esp32.query.filter_by(pinName='onlineStatus').first()
            # query.switchState = str(espstate)
            # db.session.commit()
            # print("1")

def genOTP():
    
    # global otpStartTime

    otpStartTime = time.time()

    random.seed(time.time())
    otp = random.randint(100000, 999999)

    return (otp, otpStartTime)