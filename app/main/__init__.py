from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet,configure_uploads,IMAGES
from flask_mail import Mail



login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


#extension
db = SQLAlchemy()
mail = Mail()


photos = UploadSet('photos',IMAGES)
def create_app(config_name):
    app = Flask(__name__)

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix = '/authenticate')

   # configure UploadSet
    configure_uploads(app,photos)
  # Initializing flask extensions
    db.init_app(app)
    login_manager.init_app()
    mail.init_app(app)

    return app
