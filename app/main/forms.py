from turtle import title
from unicodedata import category
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import InputRequired


class Pitchform(FlaskForm):
  title = StringField('Title', validators=[InputRequired()])
  category = SelectField('Category', choices=[('Motivation', 'Motivatio'), ('Business','Business'),('Politics', 'Politics')], validators=[InputRequired()])
  content = TextAreaField('Content', validators=[InputRequired()])
  submit = SubmitField('Pitch')