from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import getenv

app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/modules/database.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'home'

from modules import routes
