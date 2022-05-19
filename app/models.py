from datetime import datetime
from sqlalchemy import false
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(200), unique = True,nullable =False)
    email = db.Column(db.String(200),unique = True, nullable = False)   
    secure_password = db.Column(db.String(255),nullable = False)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pitch = db.relationship('Pitch', backref='user', lazy = 'dynamic')
    upvote = db.relationship('UpVote', backref='user', lazy = 'dynamic')
    downvote = db.relationship('DownVote', backref='user', lazy = 'dynamic')
    comment = db.relationship('Comment', backref='user', lazy = 'dynamic')
    

    def upvotes(self,pitch):
         return UpVote.query.filter(UpVote.user_id == self.id,UpVote.pitch_id == pitch).count() > 0
    
    def upvote_pitch(self, pitch):
        if not self.upvotes(pitch):
            upvote = UpVote(user_id=self.id, pitch_id=pitch)
            db.session.add(upvote)

    def downvotes(self,pitch):
         return DownVote.query.filter(DownVote.user_id == self.id,DownVote.pitch_id == pitch).count() > 0
    

    def downvote_pitch(self, pitch):
        if not self.downvotes(pitch):
            downvote = DownVote(user_id=self.id, pitch_id=pitch)
            db.session.add(downvote)


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.secure_password = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.secure_password,password)
    
    def save_user(self):
           db.session.add(self)
           db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'User {self.username}'



class Pitch(db.Model):
     __tablename__ = 'pitches'
     id = db.Column(db.Integer, primary_key = True)
     title = db.Column(db.String, nullable = False)
     date = db.Column(db.DateTime(timezone =True), default=func.now())
     post = db.Column(db.String, nullable = False )
     user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
     category = db.Column(db.String(255), index = True,nullable = False)
     comment = db.relationship('Comment', backref = 'pitch', lazy = "dynamic")
     upvote = db.relationship('UpVote', backref = 'pitch', lazy = "dynamic")
     downvote = db.relationship('DownVote', backref = 'pitch', lazy = "dynamic")
     
     def save_pitch(self):
           db.session.add(self)
           db.session.commit()

     
     def __repr__(self):
          return f'Pitch {self.post}'


class UpVote(db.Model):
     __tablename__ ="upvote"
     id = db.Column(db.Integer, primary_key = True)
     pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))
     user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
     
     def save(self):
           db.session.add(self)
           db.session.commit()

     @classmethod
     def get_upvotes(cls,id):
        upvote = UpVote.query.filter_by(pitch_id=id).all()
        return upvote

     def __repr__(self):
          return f'User {self.upvote}'

class DownVote(db.Model):
     __tablename__ ="downvote"
     
     id = db.Column(db.Integer, primary_key = True)
     pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))
     user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

     def save_downvote(self):
           db.session.add(self)
           db.session.commit()

     @classmethod
     def get_downvotes(cls,id):
        downvote = DownVote.query.filter_by(pitch_id=id).all()
        return downvote    

     def __repr__(self):
          return f'User {self.downvote}'
     
class Comment(db.Model):
     __tablename__= 'comments'
     id = db.Column(db.Integer, primary_key= True)
     comment = db.Column(db.String, nullable = True)
     posted = db.Column(db.DateTime,default=datetime.utcnow)
     pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))
     user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

     def save_comment(self):
           db.session.add(self)
           db.session.commit()

     @classmethod
     def get_comments(cls,pitch_id):
        comments = Comment.query.filter_by(pitch_id=pitch_id).all()

        return comments

     def __repr__(self):
          return f'User {self.comments}'
        
     @login_manager.user_loader
     def load_user(user_id):
         return User.query.get(user_id)
 