from app import db, login_manager
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
#import flask.ext.whooshalchemy as whooshalchemy

ROLE_USER = 0
ROLE_ADMIN = 1

@login_manager.user_loader
def load_user(user_id):
 return User.query.get(int(user_id))


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(120), unique = True)
    password_hash = db.Column(db.String(128))
    college = db.Column(db.String(120), default = "Universidade Federal da Bahia")
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def isAdmin(self):
        if self.role == 1:
            return True
        else:
            return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.name)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120))
    professors = db.relationship('Professor', backref = 'currentDepartment', lazy = 'dynamic')

class Post(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(5000))
    course = db.Column(db.String(120))
    ratingTeaching = db.Column(db.Integer)
    ratingEase = db.Column(db.Integer)
    gradeOnCourse = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    hideUser = db.Column(db.Boolean, default = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

class Professor(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    rating = db.Column(db.Integer)
    college = db.Column(db.String(120), default = "Universidade Federal da Bahia")
    wasAcceptedByAdmin = db.Column(db.Boolean, default = False)
    posts = db.relationship('Post', backref = 'about', lazy = 'dynamic')
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    

    def __repr__(self):
        return '<Professor %r>' % (self.first_name)