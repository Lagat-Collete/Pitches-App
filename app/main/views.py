
from dataclasses import dataclass
from flask import render_template,request,redirect,url_for,abort
from flask_login import login_required
from .. import db,photos
from . import main
from .. models import User, Pitches
from.forms import PitchForm


@main.route('/pitches', methods = ['GET','POST'])
@login_required
def pitches():
    pitches = pitches.query.ll()
    for pitch in pitches:
      print(pitch.content)
    return render_template("display_pitches.html", pitches = pitches)

@main.route('/new_pitch', methods=s['GET','POST'])
@login_required
def new_pitch():
    form = Pitchform()
    if form.validate_on_submit():
      title = form.title.data
      category = form.category.data
      content = from.content.data
      user_id = current_user._get_current_object().id
      new_pitch_object = Pitch(title = title, category = category, content = content, user_id = user_id)
      
      db.session.add(new_pitch_object)
      db.session.commit
      return redirect(url_for(app.main.index))
    return render_template('new_pitch.html', form=form)

@main.route('/user/<name>/update/pic', methods= ['POST'])
@login_required
def update_pic(name):
    user = User.query.filter_by(name = name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)
