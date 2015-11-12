from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, SelectField,IntegerField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Email, NumberRange
from .models import User, Department

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired("Campo nao pode ser em branco"), Email()])
    password = PasswordField('Password', validators=[DataRequired("Campo nao pode ser em branco")])


class RegisterForm(Form):


    name =  StringField('nameR', validators=[DataRequired("Campo nao pode ser em branco")])
    email = StringField('EmailR', validators=[DataRequired("Campo nao pode ser em branco")])
    college = StringField('Universidade', validators=[DataRequired("Campo nao pode ser em branco")])
    password = PasswordField('PasswordR', validators=[DataRequired("Campo nao pode ser em branco")])

    def validate_email(self, field):
      print(field.data)
      if User.query.filter_by(email=field.data).first():
        raise ValidationError('Email ja cadastrado.')

class RegisterProfessorForm(Form):

    name =  StringField('name', validators=[DataRequired("Campo nao pode ser em branco")])
    department = SelectField('Department', coerce = int, validators=[DataRequired("Campo nao pode ser em branco")])

    def __init__(self, *args, **kwargs):
      super(RegisterProfessorForm, self).__init__(*args, **kwargs)
      self.department.choices = [(current.id, current.name)
                                  for current in Department.query.order_by(Department.name).all()]

class BuscaForm(Form):
  department = SelectField('Department', coerce = int, validators=[DataRequired("Campo nao pode ser em branco")])

  def __init__(self, *args, **kwargs):
      super(BuscaForm, self).__init__(*args, **kwargs)
      self.department.choices = [(current.id, current.name)
                                  for current in Department.query.order_by(Department.name).all()]

class PostForm(Form):
  course = StringField('course', validators=[DataRequired("Campo nao pode ser em branco")])
  body = TextAreaField('body', validators=[DataRequired("Campo nao pode ser em branco")])
  ratingTeaching = IntegerField('ratingTeaching', validators=[NumberRange(min=0,max=10)])
  ratingEase = IntegerField('ratingEase', validators=[NumberRange(min=0,max=10)])
  gradeOnCourse = IntegerField('ratingEase', validators=[NumberRange(min=0,max=10)])
  hideUser = BooleanField('hideUser', validators=[])
