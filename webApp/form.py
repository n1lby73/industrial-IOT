#Fp = forgotten password

from app import users
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError

class loginForm (FlaskForm):
    
    email = EmailField('Email', validators=[InputRequired(), Email('Input a valid email')]) 

    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=20, message='Password must be  between 8-20 characters')])

    reg = SubmitField("Login")

class regForm (FlaskForm):
    
    username = StringField('username', validators=[InputRequired(), Length(min=5, max=20, message='username must be between 5-20 characters')])

    email = EmailField('email', validators=[InputRequired(), Email('Input a valid email')]) 

    password = PasswordField("password", validators=[InputRequired(), EqualTo("confirmpass",message="password must be the same"), Length(min=8, max=20, message='password must be  between 8-20 characters')])

    confirmpass = PasswordField("Confirm password", validators=[InputRequired(), EqualTo('password', message="passwords must be same")])

    reg = SubmitField("sign up")

    def validate_username(self, username):
        existingUserName = users.query.filter_by(username=username.data).first()

        if existingUserName:
            raise ValidationError("Username is already taken")

class  knownUserFp(FlaskForm):
    
    currentPassword = PasswordField("Current Password", validators=[InputRequired(), Length(min=8, max=20, message='Password must be  between 8-20 characters')]) 

    newPassword = PasswordField("New Password", validators=[InputRequired(), Length(min=8, max=20, message='Password must be  between 8-20 characters')])

    confirmPass = PasswordField("Confirm password", validators=[InputRequired(), EqualTo('newPassword', message="Password must be same")])
    
    reset = SubmitField("Reset")

class unKnownUserFp(FlaskForm):

    email = EmailField('Registered email', validators=[InputRequired(), Email('Input a valid email')])

    reset = SubmitField("Reset")

class forgetPassEmail(FlaskForm):

    emailOTP = PasswordField("OTP from email", validators=[InputRequired(), Length(min=6, max=6, message='OTP must contain 6 characters')]) 

    newPassword = PasswordField("New Password", validators=[InputRequired(), Length(min=8, max=20, message='Password must be  between 8-20 characters')])

    confirmPass = PasswordField("Confirm password", validators=[InputRequired(), EqualTo('newPassword', message="Password must be same")])

    reset = SubmitField("Reset")