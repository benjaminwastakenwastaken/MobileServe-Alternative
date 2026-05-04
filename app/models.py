from app import db
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
    
