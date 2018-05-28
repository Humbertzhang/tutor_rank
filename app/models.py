from flask import current_app,request
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin, current_user
from wtforms.validators import Email
from itsdangerous import JSONWebSignatureSerializer as Serializer
import base64

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(164), unique=True, index=True)
    password_hash = db.Column(db.String(164))
    school = db.Column(db.String(164))

    comments = db.relationship('Comment', backref = 'author', lazy='dynamic',cascade='all')

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm': self.id})
    
    def generate_auth_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return "<User %r>" % self.username


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(164), index = True)
    school = db.Column(db.String(164), index = True)
    research_direction = db.Column(db.String(164), index = True)
    score = db.Column(db.Float, default = 0.0)
    photo = db.Column(db.String(164), default = "https://img.laonanren.com/Public/articleimage/20180331/thum_5abefef0746a7.jpg")
    sex = db.Column(db.String(32))
    birth = db.Column(db.Integer)
    
    comments = db.relationship('Comment', backref = 'teacher', lazy='dynamic',cascade='all')

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key=True)
    score = db.Column(db.Integer)
    content = db.Column(db.Text, default = "")
    #backref teacher
    #backref author

    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
