from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#extension
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)

  # Initializing flask extensions
    db.init_app(app)
