from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.timezone import USTimeZone

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    time_zone_id = db.Column(db.Integer, db.ForeignKey('time_zone.id'))
    dst_active = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # Relationships
    messages = db.relationship('Message', backref='author', lazy='dynamic')
    time_zone = db.relationship('TimeZone')
    
    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(240))
    process_time = db.Column(db.Time)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    is_dst = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Message {self.message}>'

    def time_to_utc(self, process_time, user_id):
        tz_id = User.query.filter_by(id=user_id).first().time_zone_id
        # Make timezone object from db
        tz_db = TimeZone.query.filter_by(id=tz_id).first()
        tz = USTimeZone(tz_db.std_offset, tz_db.std_name, tz_db.std_abbr, tz_db.dst_abbr)

        # Implement a tz method that converts to UTC based on timezone considering dst. Return proper UTC time!
        

class TimeZone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    std_offset = db.Column(db.Integer)
    std_name = db.Column(db.String(64), unique=True)
    std_abbr = db.Column(db.String(16), unique=True)
    dst_abbr = db.Column(db.String(16), unique=True)

    def __repr__(self):
        return f'<TimeZone {self.std_name} {self.std_offset}>'

    
