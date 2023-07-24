from webApp.globalVar import espOnlineTimeoutq, espStartTimeq
from webApp import app, socketio, db
from webApp.models import esp32
import random
import time


# def confirmOnlinew():
    # with app.app_context():

    #     espstate

    #     # global espOnlineTimeout, espStartTime, espstate
    #     espOnlineTimeout, espStartTime

    #     currentTime = time.time()

    #     print("----------------------from function-------------------")
    #     print(espStartTime)
        
    #     if currentTime - espStartTime > espOnlineTimeout:

    #         espstate = 0
    #         socketio.emit('espOnlineState', {"value":0})
    #         query = esp32.query.filter_by(pinName='onlineStatus').first()
    #         query.switchState = str(espstate)
    #         db.session.commit()
    #         # print("0")

    #     else:

    #         print("----------------------from function-----elseee--------------")
    #         espstate = 1
    #         socketio.emit('espOnlineState', {"value":1})
    #         query = esp32.query.filter_by(pinName='onlineStatus').first()
    #         query.switchState = str(espstate)
    #         db.session.commit()
            # print("1")

def genOTP():
    
    otpStartTime = time.time()

    random.seed(time.time())
    otp = random.randint(100000, 999999)

    return (otp, otpStartTime)