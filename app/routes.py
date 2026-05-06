from flask import render_template, flash, redirect, url_for, request, abort
from app import app, db
from app.models import Admin, Student, Request
from app.forms import LoginForm, RegistrationForm
from flask_login import logout_user, login_required, current_user, login_user
from functools import wraps
from urllib.parse import urlsplit
from datetime import datetime, timezone


# Helper function to check if current user is admin
def is_admin():
    return isinstance(current_user._get_current_object(), Admin)


# Helper function to check if current user is student
def is_student():
    return isinstance(current_user._get_current_object(), Student)


# Decorator to require admin access
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        if not is_admin():
            flash('Access denied. Admins only.')
            return redirect(url_for('student_dashboard'))
        return f(*args, **kwargs)
    return decorated_function


# Decorator to require student access
def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        if not is_student():
            flash('Access denied. Students only.')
            return redirect(url_for('admin_dashboard'))
        return f(*args, **kwargs)
    return decorated_function


# Redirect to appropriate dashboard based on user type
@app.route('/')
@app.route('/index')
@login_required
def index():
    if is_admin():
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('student_dashboard'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # Try to find user in Admin table first
        user = Admin.query.filter_by(username=form.username.data).first()
        if user is None:
            # Try Student table
            user = Student.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user)

        # Redirect based on user type
        if isinstance(user, Admin):
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username already exists
        existing_admin = Admin.query.filter_by(username=form.username.data).first()
        existing_student = Student.query.filter_by(username=form.username.data).first()
        if existing_admin or existing_student:
            flash('Username already taken.')
            return redirect(url_for('register'))

        # Check if email already exists
        existing_admin = Admin.query.filter_by(email=form.email.data).first()
        existing_student = Student.query.filter_by(email=form.email.data).first()
        if existing_admin or existing_student:
            flash('Email already registered.')
            return redirect(url_for('register'))

        if form.is_admin.data:
            user = Admin(
                username=form.username.data,
                email=form.email.data
            )
        else:
            user = Student(
                username=form.username.data,
                email=form.email.data,
                grad_year=form.grad_year.data or 2025
            )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    # Show form validation errors
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{field}: {error}')

    return render_template('register.html', form=form)


# Admin dashboard - requests page (default)
@app.route('/admin')
@admin_required
def admin_dashboard():
    requests = Request.query.order_by(Request.service_date.desc()).all()
    return render_template('admin.html', requests=requests)


# Admin - student list page
@app.route('/admin/students')
@admin_required
def admin_students():
    students = Student.query.all()
    return render_template('studentList.html', students=students)


# Student dashboard
@app.route('/student')
@student_required
def student_dashboard():
    my_requests = Request.query.filter_by(student_id=current_user.id).order_by(Request.service_date.desc()).all()
    return render_template('student.html', requests=my_requests)


# Submit service hours (students only)
@app.route('/submit', methods=['GET', 'POST'])
@student_required
def submit():
    # TODO: Implement service hour request submission using the Request model
    return render_template('submit.html',  form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/user/<username>')
@login_required
def user(username):
    return render_template('user.html', user=username)
