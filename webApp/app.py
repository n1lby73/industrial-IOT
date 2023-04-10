from flask_login import LoginManager, login_required, current_user, login_user, logout_user, UserMixin
from flask import Flask, render_template, url_for, request, redirect, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from form import loginForm, knownUserFp, unKnownUserFp, forgetPassEmail
from flask_socketio import SocketIO, send, emit
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.urls import url_parse
from email.utils import formataddr
from dotenv import load_dotenv
import threading
import time
import os

load_dotenv()

app = Flask(__name__)
app.app_context().push()

app.config['MAIL_DEFAULT_SENDER'] = formataddr((os.getenv("mail_default_sender_name"), os.getenv("mail_default_sender_email")))
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['MAIL_USERNAME'] = os.getenv("mail_username")
app.config['MAIL_PASSWORD'] = os.getenv("mail_password")
app.config['MAIL_USE_SSL'] = os.getenv("mail_use_ssl")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = os.getenv("mail_server")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['MAIL_PORT'] = os.getenv("mail_port")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_DEBUG'] = True


mail = Mail(app)
db = SQLAlchemy(app)
login = LoginManager()
socketio = SocketIO(app)

login.init_app(app)
login.login_view = 'login'
login.login_message = "You're not logged in"

class esp32(db.Model):

    __tablename__ = 'motor'
    id = db.Column(db.Integer, primary_key = True)
    esp32pin = db.Column(db.String(2), nullable = False, unique = True)
    switchState = db.Column(db.String(2), nullable = False)

    def __repr__(self):
        return f'<esp32 {self.esp32pin} {self.switchState}>'

class users(UserMixin, db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), nullable = False, unique = True)
    password = db.Column(db.String(150), nullable = False)
    
    def __repr__(self):
        return f'<users {self.email} {self.password}>'

# global variables

espstate = 0
startTime = 0
timeout = 2

@login.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

@app.route('/')
@login_required
def index():

    return render_template("index.html")

@app.route('/register', methods=['POST', 'GET'])
def register():
    return "me"

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

            msg = Message('Password Recovery', recipients=['axfdsxvypceibxelzr@bbitq.com'])
            msg.body = 'did it work'
            mail.send(msg)
            flash('A password reset link has been sent to the provided email')
            return render_template("unKnownUserFp.html", form=unKnownUserForm)

        flash('Invalid email, signup instead')
        return render_template("unKnownUserFp.html", form=unKnownUserForm)
    
    return render_template("unKnownUserFp.html", form=unKnownUserForm)

@app.route('/forgetPasswordEmail', methods=['POST', 'GET'])
def forgetPasswordEmail():
    
    forgetPassEmailForm=forgetPassEmail()

    if forgetPassEmailForm.validate_on_submit():
        return "work"
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

    socketio.emit("localUpdate", value, broadcast=True)

    return jsonify(success = state)

@app.route('/btn', methods=['POST', 'GET'])
def btn():
    if request.method != 'POST':
        return redirect(url_for('index'))
    
    data = request.get_json()
    status = data['state']
    pin = data['pin']

    try:
        query = esp32.query.filter_by(esp32pin='5').first()
        
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

    global espstate, startTime

    startTime = time.time()

    return "online"

def confirmOnline():

    global timeout, startTime, espstate

    currentTime = time.time()

    if currentTime - startTime > timeout:

        espstate = 0
        socketio.emit('espOnlineState', {"value":0}, broadcast=True)
        print("0")

    else:
        espstate = 1
        socketio.emit('espOnlineState', {"value":1}, broadcast=True)
        print("1")

@socketio.on('disconnect')
def handle_disconnect():
    print("device offline")

@socketio.on('current_status')
def websocket():

    global espstate

    query = esp32.query.filter_by(esp32pin='5').first()
    state = query.switchState
    current_status_from_db = {"success":state, "value":espstate}
    socketio.emit('message', current_status_from_db, json=True, broadcast=True)
    print("A new client connected")

@socketio.on('espstatus')
def espstatus():
    while True:
        socketio.start_background_task(target=confirmOnline)
        time.sleep(0.1)

@socketio.on('update')
def websocket(update):
    state = update.get('state')
    pin  = update.get('pin')

    query = esp32.query.filter_by(esp32pin='5').first()
    
    if query:

        query.switchState = state
        db.session.commit()
        current_status_from_db = {"success":state}
        socketio.emit('message', current_status_from_db, json=True, broadcast=True)

    else:

        new_value = esp32(switchState=state, esp32pin=pin)
        db.session.add(new_value)
        db.session.commit()

        current_status_from_db = {"success":state}
        socketio.emit('message', current_status_from_db, json=True, broadcast=True)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
    # socketio.run(app, host='0.0.0.0', debug=True, port=5432)

