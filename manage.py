from flask import Flask
from app import create_app,db
from flask_script import Manager,Server
from app.models import User,Categories,Pitches,Votes,Comments
from flask_migrate import Migrate, MigrateCommand
from ..main import main_blueprint


app = create_app('development')
app = Flask(__name__)
app.register_blueprint(main_blueprint)

manager = Manager(app)
migrate = Migrate(app,db)

manager.add_command('db', MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db,User = User,Categories = Categories, Pitches = Pitches, Votes =Votes, Comments = Comments )
if __name__ == '__main__':
    manager.run()