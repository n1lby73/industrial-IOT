# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask
# from flask_login import UserMixin

# app = Flask(__name__)
# db = SQLAlchemy(app)

from app import db
from flask_login import UserMixin

class esp32(db.Model):

    __tablename__ = 'motor'
    id = db.Column(db.Integer, primary_key = True)
    esp32pin = db.Column(db.String(2), nullable = False, unique = True)
    switchState = db.Column(db.String(2), nullable = False)

    def __repr__(self):
        return '<esp32 {} {}>'.format(self.esp32pin, self.switchState)

class users(UserMixin, db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), nullable = False, unique = True)
    email = db.Column(db.String(150), nullable = False, unique = True)
    otp = db.Column(db.String(150), nullable = True, unique = True)
    role = db.Column(db.String(150), nullable = False, unique = True)
    password = db.Column(db.String(150), nullable = False)
    
    def __repr__(self):
        return '<esp32 {} {}>'.format(self.email, self.password)