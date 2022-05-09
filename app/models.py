from turtle import title
from . import db

#...

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String, unique = True)
    email = db.Column(db.String)
    

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

