from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    quotes = db.relationship('Quote', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.email}>'

class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    quote = db.Column(db.String(240))
    process_time = db.Column(db.Time)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<Quote {self.quote}>'
