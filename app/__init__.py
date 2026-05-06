# setting up flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import routes, models
from flask_login import current_user


@app.context_processor
def inject_user_type():
    def is_admin():
        if current_user.is_authenticated:
            return isinstance(current_user._get_current_object(), models.Admin)
        return False
    return dict(is_admin=is_admin)


@login_manager.user_loader
def load_user(user_id):
    # Parse the user_id format: "admin:1" or "student:1"
    if ':' in user_id:
        user_type, id_str = user_id.split(':')
        user_id_int = int(id_str)
        if user_type == 'admin':
            return models.Admin.query.get(user_id_int)
        elif user_type == 'student':
            return models.Student.query.get(user_id_int)
    return None