from email.utils import formataddr
from dotenv import load_dotenv
from webApp import app
# from flask_mail import Mail
import os

load_dotenv()

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

# class Config:
#     DEBUG = False
#     TESTING = False
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = os.getenv("SECRET_KEY")
#     MAIL_DEFAULT_SENDER = formataddr((os.getenv("mail_default_sender_name"), os.getenv("mail_default_sender_email")))
#     MAIL_USERNAME = os.getenv("mail_username")
#     MAIL_PASSWORD = os.getenv("mail_password")
#     MAIL_USE_SSL = os.getenv("mail_use_ssl")
#     MAIL_SERVER = os.getenv("mail_server")
#     MAIL_PORT = os.getenv("mail_port")
#     MAIL_USE_TLS = False
#     MAIL_DEBUG = True
#     SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")

# class ProductionConfig(Config):
#     pass

# class DevelopmentConfig(Config):
#     DEBUG = True

# class TestingConfig(Config):
#     TESTING = True

# config = {
#     'production': ProductionConfig,
#     'development': DevelopmentConfig,
#     'testing': TestingConfig
# }