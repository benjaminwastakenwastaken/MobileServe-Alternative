# setting up flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import routes, models

@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))