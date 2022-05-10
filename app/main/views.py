from crypt import methods
from flask import render_template,request,redirect,url_for,abort
from flask_login import login_required
from .. import db,photos
from . import main
from .. models import User


@main.route('/pitches/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_pitches(id):
    return render_template("pitches.html")

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
