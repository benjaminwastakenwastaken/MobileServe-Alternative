from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.models import Admin, Student, Request
from app.forms import LoginForm, RegistrationForm
from flask_login import logout_user, login_required, current_user, login_user
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
    # TODO: Implement service hour request submission using the Request model
    return redirect('/')

@app.route('/admin/alerts')
def admin_alerts():
    # TODO: Implement admin alerts view
    requests = Request.query.order_by(Request.service_date.desc()).all()
    return render_template('admin_alerts.html', requests=requests)

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
        student = Student(
            username=form.username.data,
            email=form.email.data,
            grad_year=2025  # TODO: Add grad_year to form
        )
        student.set_password(form.password.data)
        db.session.add(student)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    return render_template('user.html', user=username)

