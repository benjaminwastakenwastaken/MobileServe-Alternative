from app import db
from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms import TextAreaField
from wtforms.validators import Length
from wtforms.widgets import NumberInput
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(64))
# To understand what orgonization student have served with
# important for future steps after rough draft 
class Orgonization(db.Model)
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), index=True)
	description = db.Column(db.String(120), index=True)
	Contact_email = db.Column(db.String(120), index=True, unique=True)
    

