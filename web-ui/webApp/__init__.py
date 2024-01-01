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
# socketio = SocketIO(app, cors_allowed_origins=['http://127.0.0.1:5000','http://127.0.0.1:5500', '127.0.0.1:5500' 'https://impedo.serveo.net', 'wss://industrialiot.onrender.com', 'https://industrialiot.onrender.com', 'http://localhost:3000', 'localhost:3000', 'http://serveo.net:4565', 'serveo.net:4565', 'https://4nscf0m4-5500.uks1.devtunnels.ms'])
# # socketio = SocketIO(app, cors_allowed_origins='*',  transports=['websocket', 'xhr-polling'])

# # Use CORS for regular HTTP routes
# CORS(app, resources={r"/api/*": {"origins": [
#     'http://127.0.0.1:5000',
#     'http://127.0.0.1:5500',
#     'http://impedo.serveo.net',
#     'https://industrialiot.onrender.com',
#     'http://localhost:3000',
#     'http://localhost:5173',
#     'https://vermillion-mooncake-c13f76.netlify.app', #dev dannydoc
#     'http://serveo.net:4565'
# ]}})

socketio = SocketIO(app, cors_allowed_origins="*")
# socketio = SocketIO(app, cors_allowed_origins='*',  transports=['websocket', 'xhr-polling'])

# Use CORS for regular HTTP routes
CORS(app, resources={r"/api/*": {"origins": ["*"]}})
# CORS(app, resources={r"/api/updatepin": {"origins": "*"}})
from webApp import routes, apiRoute, socket
