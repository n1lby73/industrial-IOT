from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
socketio = SocketIO(app)

# global variable to store value if esp is online. To be used when inputting new set of value in db
esponline = 0 
class esp32(db.Model):

    __tablename__ = 'motor'
    id = db.Column(db.Integer, primary_key = True)
    esp32pin = db.Column(db.String(2), nullable = False, unique = True)
    switchState = db.Column(db.String(2), nullable = False)
    onlineStatus = db.Column(db.String(2), nullable = False)

    def __repr__(self):
        return f'<esp32 {self.esp32pin} {self.switchState}>'


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

@app.route('/online', methods=['POST', 'GET'])
def online():

    if request.method != 'POST':
        return redirect(url_for('index'))

    data = request.get_json()
    online = data['online']
    esponline = online

    query = esp32.query.filter_by(esp32pin='5').first()

    if query:

        query.onlineStatus = online
        db.session.commit()

        return jsonify(success = True)

    return jsonify(success = False)

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
        online = query.onlineStatus

        if online == 1:

            online = 0
            query.switchState = status
            query.onlineStatus = online

            db.session.commit()

            return jsonify(success=True)
        
        else:

            return jsonify(success=False)
            
    if esponline == 1:

        new_value = esp32(switchState=status, esp32pin=pin, onlineStatus=esponline)

        db.session.add(new_value)
        db.session.commit()

        return jsonify(success=True)
    
    return "esp not up"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3565)