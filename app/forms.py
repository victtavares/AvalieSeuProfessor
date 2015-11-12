from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterForm(Form):
    name =  StringField('name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    university = StringField('Universidade', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

