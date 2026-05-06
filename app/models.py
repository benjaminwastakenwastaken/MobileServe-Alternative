from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def get_id(self):
        return f'admin:{self.id}'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Admin {self.username}>'


class Student(UserMixin, db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    hours_indirect = db.Column(db.Integer, default=0)
    hours_direct = db.Column(db.Integer, default=0)
    grad_year = db.Column(db.Integer, nullable=False)

    # Relationship to requests
    requests = db.relationship('Request', backref='student', lazy='dynamic')

    def get_id(self):
        return f'student:{self.id}'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Student {self.username}>'


class Request(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    details = db.Column(db.String(500), nullable=False)
    direct = db.Column(db.Boolean, default=False)
    organization = db.Column(db.String(128), nullable=False)
    organization_contact = db.Column(db.String(256))
    service_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Request {self.id} by Student {self.student_id}>'
