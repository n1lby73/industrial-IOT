from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from webApp import db

class esp32(db.Model):

    __tablename__ = 'motor'
    id = db.Column(db.Integer, primary_key = True)
    esp32pin = db.Column(db.String(2), nullable = False, unique = True)
    pinFunction = db.Column(db.String(200), nullable = False, unique = True)
    pinName = db.Column(db.String(200), nullable = False, unique = True)
    switchState = db.Column(db.String(2), nullable = False)

    def __repr__(self):
        return '<esp32 {} {}>'.format(self.esp32pin, self.switchState)

class users(UserMixin, db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), nullable = False, unique = True)
    email = db.Column(db.String(150), nullable = False, unique = True)
    role = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String(150), nullable = False)
    token = db.Column(db.String(5000), nullable = True)
    otp = db.Column(db.String(6), nullable = True)
    verifiedEmail = db.Column(db.String(5), nullable = True, default = "False")
    
    def __repr__(self):
        return '<esp32 {} {}>'.format(self.email, self.password)
