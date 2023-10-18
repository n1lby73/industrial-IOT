from dotenv import load_dotenv
from datetime import timedelta
from webApp import app
import os

load_dotenv()

app.config['MAIL_DEFAULT_SENDER'] = os.getenv('mail_default_sender')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['CACHE_DEFAULT_TIMEOUT'] = int(os.getenv("CACHE_DEFAULT_TIMEOUT"))
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=10)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)
app.config['CACHE_TYPE'] = os.getenv("CACHE_TYPE")
app.config['MAIL_USERNAME'] = os.getenv("mail_username")
app.config['MAIL_PASSWORD'] = os.getenv("mail_password")
app.config['MAIL_USE_SSL'] = os.getenv("mail_use_ssl")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = os.getenv("mail_server")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['MAIL_PORT'] = os.getenv("mail_port")
# app.config["JWT_COOKIE_SECURE"] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_DEBUG'] = True
# app.config["JWT_TOKEN_LOCATION"] = "cookies"