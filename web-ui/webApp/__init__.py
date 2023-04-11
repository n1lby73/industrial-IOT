from flask_socketio import SocketIO, send, emit
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from email.utils import formataddr
from flask_mail import Mail
from flask import Flask
import os

app = Flask(__name__)
app.app_context().push()

from webApp import config

db = SQLAlchemy(app)
mail = Mail(app)
login = LoginManager()
socketio = SocketIO(app)

from webApp import routes