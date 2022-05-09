from enum import unique
from operator import index
from werkzeug.security import generate_password_hash,check_password_hash
from turtle import title
from . import db
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String, unique = True)
    email = db.Column(db.String(200),unique = True, index = True)
    pass_secure = db.Column(db.String(200))

@property
def password(self):
     raise AttributeError('You cannot read the password attribute')

@password.setter
def password(self, password):
     self.pass_secure = generate_password_hash(password)

def verify_password(self,password):
            return check_password_hash(self.pass_secure,password)
def __repr__(self):
        return f'User {self.username}'

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)

class Pitches(db.Model):
     id = db.Column(db.Integer, primary_key = True)
     title = db.Column(db.String, nullable = False)
     body = db.Column(db.Text, nullable = False )
     user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
     user = db.relationship('User', backref = db.backref('pitches'))
     category_id = db.Column(db.Integer, db.ForeignKey('categories_id'))
     category = db.relationship(Categories, backref=db.backref('pitches'))
     votes_id = db.Column(db.Integer, db.ForeignKey('votes.id'))
     votes = db.relationship('votes', backref=db.backref('pitches', lazy = True))
     comment_id = db.Column(db.Integer,db.ForeignKey('comments.id'))
     comments = db.relationship('Comments', backref = db.backref('pitches'))



class Votes(db.Model):
     id = db.Column(db.Integer, primary_key = True)
     down_votes = db.Column(db.Integer)
     up_votes = db.Column(db.Integer)

class Comments(db.Model):
     id = db.Column(db.Integer, primary_key = True)
     comment = db.Column(db.text)

