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

class Alert(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	action = db.Column()
    
# basic user outline for Routes login
class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(128), index=True,
                                             unique=True)
    # Should not care abt saftey or password hash for rough draft 
    password: so.Mapped[str] = so.mapped_column(sa.String(256))
