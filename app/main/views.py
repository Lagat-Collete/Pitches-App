from dataclasses import dataclass
from flask import render_template,request,redirect,url_for,abort
from flask_login import login_required
from .. import db,photos
from . import main
from .. models import User, Pitch,UpVote,DownVote,Comment
from.forms import  CommentForm, PitchForm,current_user


@main.route('/')
def index():
    pitches = pitches.query.ll()
    games= Pitch.query.filter_by(category = 'Games').all() 
    business = Pitch.query.filter_by(category = 'Business').all()
    education = Pitch.query.filter_by(category = 'Education').all()
    return render_template("index.html",games= games,business=business,education=education )

@main.route('/new_pitch', methods=['GET','POST'])
@login_required
def new_pitch():
    form = PitchForm()
    if form.validate_on_submit():
      title = form.title.data
      category = form.category.data
      content = form.content.data
      user_id = current_user._get_current_object().id
      new_pitch_object = Pitch(title = title, category = category, content = content, user_id = user_id)
      db.session.add(new_pitch_object)
      db.session.commit
      return redirect(url_for(app.main.index))
    return render_template('new_pitch.html', form=form)


@main.route('/comment/<int:pitch_id>', methods = ['POST','GET'])
@login_required
def comment(pitch_id):
    form = CommentForm()
    pitch = Pitch.query.get(pitch_id)
    all_comments = Comment.query.filter_by(pitch_id = pitch_id).all()
    if form.validate_on_submit():
        comment = form.comment.data 
        pitch_id = pitch_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment = comment,user_id = user_id,pitch_id = pitch_id)
        new_comment.save_comment()
        return redirect(url_for('.comment', pitch_id = pitch_id))
    return render_template('comment.html', form =form, pitch = pitch,all_comments=all_comments)

@main.route


@main.route('/user/<name>/update/pic', methods= ['POST'])
@login_required
def update_pic(name):
    user = User.query.filter_by(username = name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)
