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
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(200))
    pitch = db.relationship('Pitches', backref='user', lazy = 'dynamic')
    upvote = db.relationship('UpVotes', backref='user', lazy = 'dynamic')
    downvote = db.relationship('DownVotes', backref='user', lazy = 'dynamic')
    comment = db.relationship('Comments', backref='user', lazy = 'dynamic')

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
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    pitch = db.relationship('Pitches', backref = 'category', lazy = 'dynamic')



class Pitches(db.Model):
     __tablename__ = 'pitches'
     id = db.Column(db.Integer, primary_key = True)
     title = db.Column(db.String, nullable = False)
     body = db.Column(db.Text, nullable = False )
     user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
     category = db.Column(db.Integer, db.ForeignKey('categories.id'))
     upvote = db.relationship('UpVotes', backref = 'pitches', lazy = "dynamic")
     downvote = db.relationship('DownVotes', backref = 'pitches', lazy = "dynamic")
     comment = db.relationship('Comments', backref = 'pitches', lazy = "dynamic")
     
     def save_pitch(self):
           db.session.add(self)
           db.session.commit()

class UpVotes(db.Model):
     __tablename__ ="upvote"
     id = db.Column(db.Integer, primary_key = True)
     up_votes = db.Column(db.Integer)
     pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))
     user_id = db.Column(db.Integer,db.ForeignKey("users.id"))


class DownVotes(db.Model):
     __tablename__ ="downvote"
     id = db.Column(db.Integer, primary_key = True)
     down_votes = db.Column(db.Integer)
     pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))
     user_id = db.Column(db.Integer,db.ForeignKey("users.id"))


     
class Comments(db.Model):
     __tablename__= 'comments'
     id = db.Column(db.Integer, primary_key = True)
     comment = db.Column(db.text)
     pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))
     user_id = db.Column(db.Integer,db.ForeignKey("users.id"))



