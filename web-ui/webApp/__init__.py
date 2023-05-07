from flask_socketio import SocketIO, send, emit
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_mail import Mail
from flask import Flask
#import socketio

app = Flask(__name__)
app.app_context().push()

from webApp import config

db = SQLAlchemy(app)
mail = Mail(app)
login = LoginManager()
socketio = SocketIO(app, cors_allowed_origins='*')
#sio = socketio.AsyncServer()

from webApp import routes
