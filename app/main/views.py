from crypt import methods
from flask_login import login_required

@main.route('/pitches/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_pitches(id):