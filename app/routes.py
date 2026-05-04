from flask import render_template
from app import app
from flask import render_template, flash, redirect, url_for
import sqlalchemy as sa
from app import db
from app.forms import LoginForm, RegistrationForm
from flask_login import logout_user, login_required, login_user, current_user
from app.models import User
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
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)
    

# https://www.geeksforgeeks.org/python/flask-http-method/
@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')

    alert = Alert(
        action =="submission",
        details==f"{username} submitted a service hour" #what the alert says
    )

    db.session.add(alert)
    db.session.commit()

    return redirect('/')

@app.route('/admin/alerts')
def admin_alerts():
    alerts = Alert.query.order_by(Alert.created_at.desc()).all()
    return render_template('admin_alerts.html', alerts=alerts)

@app.route('/logTime')
@login_required
def logTime():
    return "Log Time Page"  # TODO: implement log time form

@app.route('/logout')
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

