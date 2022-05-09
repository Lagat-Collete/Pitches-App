from flask import render_template,request,redirect,url_for,abort
from flask_login import login_required

@main.route('/pitches/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_pitches(id):

@main.route('/user/<name>')
def profile(name):
    user = User.query.filter_by(name = name).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)
