from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_socketio import SocketIO, send, emit
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import threading
import time
import os

load_dotenv()

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
socketio = SocketIO(app)

class esp32(db.Model):

    __tablename__ = 'motor'
    id = db.Column(db.Integer, primary_key = True)
    esp32pin = db.Column(db.String(2), nullable = False, unique = True)
    switchState = db.Column(db.String(2), nullable = False)

    def __repr__(self):
        return f'<esp32 {self.esp32pin} {self.switchState}>'

class users(db.Model):

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

@app.route('/')
def index():

    return render_template("index.html")

@app.route('/login')
def login():
    a=login
@app.route('/query', methods=['POST', 'GET'])
def query():

    if request.method != 'POST':
        return redirect(url_for('index'))
         
    query = esp32.query.filter_by(esp32pin='5').first()
    state = query.switchState
    # socketio.start_background_task(target=confirmOnline)
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

