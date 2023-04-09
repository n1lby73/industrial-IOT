#Fp = forgotten password

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo

class loginForm (FlaskForm):
    
    email = EmailField('Email', validators=[InputRequired(), Email('Input a valid email')]) 

    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=20, message='Password must be  between 8-20 characters')])

    reg = SubmitField("Login")

class  knownUserFp(FlaskForm):
    
    currentPassword = PasswordField("Current Password", validators=[InputRequired(), Length(min=8, max=20, message='Password must be  between 8-20 characters')]) 

    newPassword = PasswordField("New Password", validators=[InputRequired(), Length(min=8, max=20, message='Password must be  between 8-20 characters')])

    confirmPass = PasswordField("Confirm password", validators=[InputRequired(), EqualTo('newPassword', message="Password must be same")])
    
    reset = SubmitField("Reset")

class unKnownUserFp(FlaskForm):

    email = EmailField('Registered email', validators=[InputRequired(), Email('Input a valid email')])

    reset = SubmitField("Reset")