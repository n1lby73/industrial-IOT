from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo

class loginForm (FlaskForm):
    
    email = EmailField('Email', validators=[InputRequired(), Email('Input a valid email')]) 

    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=20, message='Password must be  between 8-20 characters')])

    reg = SubmitField("Login")
