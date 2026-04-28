from app import db
from datetime import datetime

class Alert(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	action = db.Column()