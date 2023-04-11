from flask import Flask
from flask_socketio import SocketIO, send, emit
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from dotenv import load_dotenv
# from webApp.config import config
from flask_login import LoginManager
from email.utils import formataddr
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

# app.config.from_object(config['development'])

db = SQLAlchemy(app)
mail = Mail(app)
login = LoginManager()
socketio = SocketIO(app)

from webApp import routes