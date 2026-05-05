from flask import render_template
from app import app
from flask import render_template, flash, redirect, url_for
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models import Alert,User
from app.forms import LoginForm, SubmitForm, RegistrationForm
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user
from flask import request
from urllib.parse import urlsplit
from datetime import datetime, timezone



# creating the first page
@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # basic should make it work for rough draft 
    # need to make database and load_user protocoll
    if form.validate_on_submit():
        return redirect(url_for('index'))
        # TODO: Add actual login logic here
        flash('Login requested for user {}'.format(form.username.data))
    return render_template('login.html', form=form)
    

# https://www.geeksforgeeks.org/python/flask-http-method/
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    
    form = SubmitForm()

    if request.method == 'POST':

        username = request.form.get('username')

        alert = Alert(
            action ="submission",
            details=f"{username} submitted a service hour" #what the alert says
        )

        db.session.add(alert)
        db.session.commit()

        return render_template('submit.html', form=form)
    return render_template('submit.html', form=form)


@app.route('/admin/alerts')
def admin_alerts():
    alerts = Alert.query.order_by(Alert.created_at.desc()).all()
    return render_template('admin_alerts.html', alerts=alerts)

@app.route('/logTime')
@login_required
def logTime():
    return "Log Time Page"  # TODO: implement log time form

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    return render_template('user.html', user=username)

