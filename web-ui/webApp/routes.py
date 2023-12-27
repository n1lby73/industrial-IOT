from webApp.form import loginForm, knownUserFp, unKnownUserFp, forgetPassEmail, regForm, confirmEmail, validEmail
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, decode_token, jwt_manager
from flask import render_template, url_for, request, redirect, jsonify, flash, current_app
from flask_login import login_required, current_user, login_user, logout_user, UserMixin
from webApp.globalVar import otpTimeout 
from werkzeug.security import generate_password_hash, check_password_hash
from webApp import app, db, mail, login, socketio, jwt
from webApp.function import  genOTP
from webApp.models import users, esp32
from werkzeug.urls import url_parse
from flask_mail import Message
from datetime import timedelta
import random, time


login.init_app(app)
login.login_view = 'login'
login.login_message = "You're not logged in"

# espstate = 1
# espStartTime = 0
# espOnlineTimeout = 60

# def confirmOnline():
#     with app.app_context():

#         # espstate

#         # global espOnlineTimeout, espStartTime, espstate
#         global espOnlineTimeout, espStartTime, espstate

#         currentTime = time.time()

#         print("----------------------from function-------------------")
#         print(espStartTime)
#         print(espOnlineTimeout)
#         print(currentTime)
#         if currentTime - espStartTime > espOnlineTimeout:

#             espstate = 0
#             socketio.emit('espOnlineState', {"value":0})
#             # query = esp32.query.filter_by(pinName='onlineStatus').first()
#             # query.switchState = str(espstate)
#             # db.session.commit()
#             # print("0")

#         else:

#             print("----------------------from function-----elseee--------------")
#             espstate = 1
#             socketio.emit('espOnlineState', {"value":1})
            # query = esp32.query.filter_by(pinName='onlineStatus').first()
            # query.switchState = str(espstate)
            # db.session.commit()
            # print("1")

@login.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

@app.route('/')
@login_required
def index():

    if current_user.verifiedEmail != "True":

        flash("Check regisered email for OTP")
        return redirect(url_for('email'))
    
    if current_user.role != "owner":
        
        return render_template('index.html')

    regUser = users.query.with_entities(users.id, users.username, users.email, users.role).all()

    return render_template("index.html", form=regUser)

@app.route('/register', methods=['POST', 'GET'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form=regForm()
    emailForm = confirmEmail()

    if form.validate_on_submit():

        email = request.form.get('email')
        username = request.form.get('username') 
        password = request.form.get('password')

        new_user = users(email=email, username=username, role="user", password=generate_password_hash(password))

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':

            next_page = url_for('email')

        return redirect(next_page)

    return render_template("signup.html", form=form)

@app.route('/email', methods=['POST', 'GET'])
def email():

    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    verify=confirmEmail()

    if verify.validate_on_submit():

        global otpStartTime, otpTimeout

        collectedOtp = str(request.form.get('emailOTP'))

        currentTime = time.time()

        if (currentTime - otpStartTime) > otpTimeout:

            current_user.otp = " "
            db.session.commit()

            flash ("Expired otp, request for a new one")
            return render_template("confirmEmail.html", form=verify, email=current_user.email)
        
        if current_user.otp != collectedOtp:

            flash ("invalid otp entered")
            return render_template("confirmEmail.html", form=verify, email=current_user.email)
        
        current_user.otp = " "
        current_user.verifiedEmail = "True"

        db.session.commit()

        logout_user()

        flash ("Verification Successful, login now")
        return redirect(url_for("login"))
    
    email = current_user.email

    otp, otpStartTime = genOTP()
    
    current_user.otp = str(otp)
    
    db.session.commit()

    msg = Message('Email Verification', recipients=[email])
    msg.html = render_template("emailVerification.html", otp=otp)
    mail.send(msg)

    flash("check your email "+ email +" for your otp to complete registration")

    return render_template("confirmEmail.html", form=verify, email=email)

@app.route('/typoEmail', methods=['POST', 'GET'])
def typoEmail():

    if not current_user.is_authenticated or current_user.verifiedEmail == "True":

        return render_template('404.html')
    
    newEmail = validEmail()

    if newEmail.validate_on_submit():

        email = request.form.get('email')

        current_user.email = email

        db.session.commit()

        return redirect(url_for('email'))
    
    return render_template("typoEmail.html", form=newEmail)

@app.route('/login', methods=['POST', 'GET'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form=loginForm()

    if form.validate_on_submit():

        email = request.form.get('email')
        password = request.form.get('password')
        
        user = users.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):

            flash('Please check your login details and try again.')

            return render_template("signin.html", form=form)
        
        login_user(user)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':

            next_page = url_for('index')

        return redirect(next_page)
    
    return render_template("signin.html", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/forgetPassword', methods=['POST', 'GET'])
def forgetPassword():
    
    knownUserForm=knownUserFp()
    unKnownUserForm=unKnownUserFp()

    if current_user.is_authenticated:

        if knownUserForm.validate_on_submit():
                
                oldpass = request.form.get('currentPassword')
                newpass = request.form.get('newPassword')

                email = users.query.filter_by(email=current_user.email).first()

                if not check_password_hash(email.password, oldpass):

                    flash("incorrect password")
                    return render_template("knownUserFp.html", form=knownUserForm)
                
                email.password = generate_password_hash(newpass)
                db.session.commit()

                return redirect(url_for('index'))
        
        return render_template("knownUserFp.html", form=knownUserForm)
    
    if unKnownUserForm.validate_on_submit():
        email = request.form.get('email')

        confirmEmail = users.query.filter_by(email=email).first()

        if confirmEmail:

            loggedUser = {"email":email, "username":confirmEmail.username, "role":confirmEmail.role}
            access_token = create_access_token(identity=loggedUser, expires_delta=timedelta(seconds=120))

            confirmEmail.token = access_token
            db.session.commit()

            msg = Message('Password Recovery', recipients=[email])
            msg.html = render_template("resetLink.html", username=confirmEmail.username, link=access_token)
            mail.send(msg)
            flash('A password reset link has been sent to the provided email')
            return render_template("unKnownUserFp.html", form=unKnownUserForm)

        flash('Invalid email, signup instead')
        return render_template("unKnownUserFp.html", form=unKnownUserForm)
    
    return render_template("unKnownUserFp.html", form=unKnownUserForm)

@app.route('/forgetPasswordEmail/<token>', methods=['POST', 'GET'])
def forgetPasswordEmail(token):
    
    forgetPassEmailForm=forgetPassEmail()
    unKnownUserForm=unKnownUserFp()

    try:

        decoded_token = decode_token(token)

        payload = decoded_token['sub']

        email = payload['email']

        verifyEmail = users.query.filter_by(email=email).first()

        if verifyEmail.token != token:
            
            return render_template("404.html")
    
    except:

        return render_template("404.html")
    
    if verifyEmail:

        if forgetPassEmailForm.validate_on_submit():
            
            newpass = request.form.get('confirmPass')
            verifyEmail.password = generate_password_hash(newpass)
            verifyEmail.token = " "
            db.session.commit()

            flash("Password updated successfully, please log in")
            return redirect(url_for('login'))
        
    return render_template("forgetPassEmail.html", form=forgetPassEmailForm)

@app.route('/query', methods=['POST', 'GET'])
def query():

    if request.method != 'POST':
        return redirect(url_for('index'))
         
    query = esp32.query.filter_by(esp32pin='5').first()
    state = query.switchState
    return jsonify(success = state)

@app.route('/synchardchanges', methods=['POST', 'GET'])
def synchardchanges():

    if request.method != 'POST':
        return redirect(url_for('index'))
    
    data = request.get_json()
    status = data['state']
    pin = data['pin']

    query = esp32.query.filter_by(esp32pin='5').first()
    state = query.switchState

    if state != status:

        query.switchState = status
        db.session.commit()
        state = status
        value = {"update":state}

    socketio.emit("localUpdate", value)

    return jsonify(success = state)

@app.route('/btn', methods=['POST', 'GET'])
def btn():
    if request.method != 'POST':
        return redirect(url_for('index'))
    
    data = request.get_json()
    status = data['state']
    pin = data['pin']

    try:
        query = esp32.query.filter_by(esp32pin=pin).first()
        
        if query:

            query.switchState = status
            db.session.commit()
            
            return jsonify(success=True)
    except:
        new_value = esp32(switchState=status, esp32pin=pin)

        db.session.add(new_value)
        db.session.commit()
        
        return jsonify(success=True)

@app.route('/espOnline', methods=['POST', 'GET'])
def espOnline():

    if request.method != 'POST':
        return redirect(url_for('index'))

    global espStartTime
    # espStartTime
    print("-----------------------------from route----------------")
    
    espStartTime = time.time()
    print (espStartTime)
    socketio.emit('espstatus')
    return "online"

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
   print("device offline")

@socketio.on('current_status')
def websocket():

    # global espstate
    # espstate
    query = esp32.query.filter_by(esp32pin='5').first()
    state = query.switchState

    socketio.emit('currentUpdate', {"success":state, "value":1})
    print (state)
    print("A new client connected")

@socketio.on('espstatus')
def espstatus():
    socketio.emit('espOnlineState', {"value":1})
#     with current_app.app_context():
#         while True:
#             socketio.start_background_task(target=confirmOnline)
#             time.sleep(0.1)

@socketio.on('update')
def websocket(update):
    state = update.get('state')
    pin  = update.get('pin')

    query = esp32.query.filter_by(esp32pin='5').first()
    
    if query:

        query.switchState = state
        db.session.commit()
        current_status_from_db = {"success":state}
        # socketio.emit('message', current_status_from_db, json=True, broadcast=True)
        socketio.emit('message', current_status_from_db)

    else:

        new_value = esp32(switchState=state, esp32pin=pin)
        db.session.add(new_value)
        db.session.commit()

        current_status_from_db = {"success":state}
        # socketio.emit('message', current_status_from_db, json=True, broadcast=True)
        socketio.emit('message', current_status_from_db)

# @socketio.on('role')
# def websocket():
#     socketio.emit('storeRole',{"role":current_user.role})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')
