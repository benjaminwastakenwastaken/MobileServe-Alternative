from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from app import db
from wtforms import TextAreaField
from wtforms.validators import Length
from wtforms.widgets import NumberInput

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    grad_year = IntegerField('Graduation Year', widget=NumberInput(min=2020, max=2035))
    is_admin = BooleanField('Register as Admin')
    submit = SubmitField('Register')

class SubmitForm(FlaskForm):
        hours = IntegerField('How many hours of of service ', widget=NumberInput(min=0))
        details = TextAreaField('What did you do? And who did you impact', validators=[Length(min=0)])
        Org = TextAreaField('Who did you serve with', validators=[Length(min=0)])
        type  = BooleanField('Was this direct service or not ')
        submit = SubmitField('Submit')