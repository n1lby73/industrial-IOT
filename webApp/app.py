from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send, emit
from dotenv import load_dotenv
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
# socketio = SocketIO(app, cors_allowed_origins="*")

class esp32(db.Model):

    __tablename__ = 'motor'
    id = db.Column(db.Integer, primary_key = True)
    esp32pin = db.Column(db.String(2), nullable = False, unique = True)
    switchState = db.Column(db.String(2), nullable = False)

    def __repr__(self):
        return f'<esp32 {self.esp32pin} {self.switchState}>'

# global variables

espstate = 0

@app.route('/')
def index():

    return render_template("index.html")


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

    query = esp32.query.filter_by(esp32pin='5').first()
    
    if query:

        query.switchState = status
        db.session.commit()
        
        return jsonify(success=True)

    new_value = esp32(switchState=status, esp32pin=pin)

    db.session.add(new_value)
    db.session.commit()
    
    return jsonify(success=True)

# @socketio.on('connect')
# def handle_connect():
#     query = esp32.query.filter_by(esp32pin='5').first()
#     state = query.switchState
#     current_status = {"success":state}
#     socketio.emit('message', current_status, broadcast=True)
#     print("A new client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("device offline")

@socketio.on('current_status')
def websocket():

    global espstate

    query = esp32.query.filter_by(esp32pin='5').first()
    state = query.switchState
    current_status_from_db = {"success":state, "onlineStatus":espstate}
    socketio.emit('message', current_status_from_db, json=True)
    print("A new client connected")

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


@socketio.on('espOnline')
def websocket(espOnlinie):
    global espstate
    espstate = 1
    print ("espstateggh is ", espstate)
# Background task to monitor incoming data
def espOffline():

    global espstate

    # Set a timeout period of 5 seconds
    timeout_period = 1
    start_time = time.time()

    while True:
        # Check if the timeout period has elapsed
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout_period:
            # Carry out some task if no data is received in the given time frame
            # print('No data received in the given time frame')
            # global espstate
            espstate = 0
            start_time = time.time()

        # else:
        #     espstate = 1
        # Wait for 1 second before checking again
        time.sleep(1)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ == '__main__':
    socketio.start_background_task(espOffline)
    socketio.run(app, host='0.0.0.0')
    # socketio.run(app, debug=True, port=3565, host='0.0.0.0')
    # app.run(host='0.0.0.0', debug=True, port=3565)