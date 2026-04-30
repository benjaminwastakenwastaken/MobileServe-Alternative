from flask import render_template
from app import app
from flask import render_template, flash, redirect, url_for
import sqlalchemy as sa
from app import db
from app.forms import LoginForm
from flask_login import logout_user
from flask_login import login_required
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
    form = LoginForm()
    if form.validate_on_submit():
        # TODO: Add actual login logic here
        flash('Login requested for user {}'.format(form.username.data))
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

