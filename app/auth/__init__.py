from flask import Blueprint
aouth = Blueprint('auth',__name__)
from . import views,forms