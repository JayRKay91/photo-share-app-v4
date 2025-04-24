from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    photos = db.relationship('Photo', backref='owner', lazy=True)
    shared_access = db.relationship('SharedAccess', backref='primary_user', lazy=True)

class SharedAccess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_name = db.Column(db.String(80), nullable=False)  # e.g. “Mom”
    email = db.Column(db.String(120), nullable=False)
    primary_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    can_upload = db.Column(db.Boolean, default=True)
    can_comment = db.Column(db.Boolean, default=True)

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='photo', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'), nullable=False)
    author_name = db.Column(db.String(80), nullable=False)  # e.g. “Mom”
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
