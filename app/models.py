from datetime import datetime
from email.policy import default
from enum import unique
from operator import index
from sqlalchemy.sql import func
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
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(200))
    pitch = db.relationship('Pitch', backref='user', lazy = 'dynamic')
    upvote = db.relationship('UpVotes', backref='user', lazy = 'dynamic')
    downvote = db.relationship('DownVotes', backref='user', lazy = 'dynamic')
    comment = db.relationship('Comments', backref='user', lazy = 'dynamic')
    
    def save_user(self):
           db.session.add(self)
           db.session.commit()

    def upvotes(self,pitch):
         return UpVotes.query.filter(UpVotes.user_id == self.id,UpVotes.pitch_id == pitch).count() > 0
    
    def upvote_pitch(self, pitch):
        if not self.upvotes(pitch):
            upvote = UpVotes(user_id=self.id, pitch_id=pitch)
            db.session.add(upvote)

    def downvotes(self,pitch):
         return DownVotes.query.filter(DownVotes.user_id == self.id,DownVotes.pitch_id == pitch).count() > 0
    

    def downvote_pitch(self, pitch):
        if not self.downvotes(pitch):
            downvote = DownVotes(user_id=self.id, pitch_id=pitch)
            db.session.add(downvote)


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
    
    def save_category(self):
           db.session.add(self)
           db.session.commit()
          
    def __repr__(self):
            return f'User {self.category}'


class Pitch(db.Model):
     __tablename__ = 'pitches'
     id = db.Column(db.Integer, primary_key = True)
     title = db.Column(db.String, nullable = False)
     date = db.Column(db.DateTime(timezone =True), default=func.now())
     body = db.Column(db.Text, nullable = False )
     user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
     category = db.Column(db.Integer, db.ForeignKey('categories.id'))
     upvote = db.relationship('UpVotes', backref = 'pitch', lazy = "dynamic")
     downvote = db.relationship('DownVotes', backref = 'pitch', lazy = "dynamic")
     comment = db.relationship('Comments', backref = 'pitch', lazy = "dynamic")
    
     def save_pitch(self):
           db.session.add(self)
           db.session.commit()

     def get_pitches(id):
        pitches = Pitch.query.filter_by(category=id).all()
        return pitches

     def __repr__(self):
            return f'User {self.pitch}'


class UpVotes(db.Model):
     __tablename__ ="upvote"
     id = db.Column(db.Integer, primary_key = True)
     up_votes = db.Column(db.Integer)
     pitch_id = db.Column(db.Integer, db.ForeignKey('pitch.id'))
     user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
     
     def save_upvote(self):
           db.session.add(self)
           db.session.commit()
    
     def __repr__(self):
            return f'User {self.upvotes}'

class DownVotes(db.Model):
     __tablename__ ="downvote"
     id = db.Column(db.Integer, primary_key = True)
     down_votes = db.Column(db.Integer)
     pitch_id = db.Column(db.Integer, db.ForeignKey('pitch.id'))
     user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

     def save_downvote(self):
           db.session.add(self)
           db.session.commit()

     def __repr__(self):
            return f'User {self.downvotes}'
     
class Comments(db.Model):
     __tablename__= 'comments'
     id = db.Column(db.Integer, primary_keyneetcodeneetcode = True)
     comment = db.Column(db.text)
     posted = db.Column(db.DateTime,default=datetime.utcnow)
     pitch_id = db.Column(db.Integer, db.ForeignKey('pitch.id'))
     user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

     def save_comments(self):
           db.session.add(self)
           db.session.commit()

     def __repr__(self):
          return f'User {self.comments}'
     @classmethod
     def get_comments(cls,id):
         comments = Comments.query.filter_by(pitch_id=id).all()
         return comments
        

