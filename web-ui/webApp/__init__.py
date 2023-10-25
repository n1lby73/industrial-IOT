from flask_socketio import SocketIO, send, emit
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from flask_mail import Mail
from flask import Flask
import socketio

app = Flask(__name__)
app.app_context().push()

from webApp import config

db = SQLAlchemy(app)
api = Api(app)
mail = Mail(app)
jwt = JWTManager(app)
login = LoginManager()
migrate = Migrate(app, db)
socketio = SocketIO(app, cors_allowed_origins=['http://127.0.0.1:5000', 'https://impedo.serveo.net', 'wss://industrialiot.onrender.com', 'https://industrialiot.onrender.com'])
# socketio = SocketIO(app, cors_allowed_origins='*',  transports=['websocket', 'xhr-polling'])


from webApp import routes, apiRoute
