
from flask import render_template,request,redirect,url_for,abort
from flask_login import login_required,current_user
from .. import db,photos
from . import main
from .. models import User, Pitch,UpVote,DownVote,Comment
from.forms import  CommentForm, PitchForm, UpdateProfile



@main.route('/')
@login_required
def index():
    pitches = Pitch.query.all()
    
    return render_template("index.html",pitches = pitches)

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
      return redirect(url_for('.index'))
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

@main.route('/like/<int:id>',methods = ['POST','GET'])
@login_required
def like(id):
    get_pitches = UpVote.get_upvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for pitch in get_pitches:
        to_str = f'{pitch}'
        print(valid_string+' '+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_vote = UpVote(user = current_user, pitch_id=id)
    new_vote.save()
    return redirect(url_for('main.index',id = id))

@main.route('/dislike/<int:id>',methods = ['POST','GET'])
@login_required
def dislike(id):
    get_pitches = DownVote.get_downvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for pitch in get_pitches:
        to_str = f'{pitch}'
        print(valid_string+' '+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_vote = DownVote(user = current_user, pitch_id=id)
    new_vote.save()
    return redirect(url_for('main.index',id = id))


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    user_id = current_user._get_current_object().id
    posts = Pitch.query.filter_by(user_id = user_id).all()
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,posts=posts)

@main.route('/user/<uname>/updateprofile', methods = ['POST','GET'])
@login_required
def updateprofile(uname):
    form = UpdateProfile()
    user = User.query.filter_by(username = uname).first()
    if user == None:
        abort(404)

    if form.validate_on_submit():
        user.bio = form.bio.data
        
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname = user.username))
    return render_template('profile/update.html',form =form)



@main.route('/user/<uname>/update/pic', methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()

        return redirect(url_for('main.profile',uname=uname))

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)
