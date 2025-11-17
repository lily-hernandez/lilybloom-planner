# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(10), nullable=False)   # format: YYYY-MM-DD
    start_time = db.Column(db.String(5), nullable=True)  # HH:MM
    end_time = db.Column(db.String(5), nullable=True)
    category = db.Column(db.String(50), nullable=False)  # work, school, gym, family, other
    notes = db.Column(db.Text, nullable=True)

class DailyNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    content = db.Column(db.Text, nullable=True)

class GymLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    went = db.Column(db.Boolean, default=True)
