from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    resumes = db.relationship('Resume', backref='user', lazy=True)
    listings = db.relationship('Listing', backref='user', lazy=True)

    def __repr__(self):
        return f"User: {self.username}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Resume(db.Model):
    resume_id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(64), index=True, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),
              nullable=False)
    listings = db.relationship('Listing', backref='resume', lazy=True)

    def __repr__(self):
        return f"Resume file name: {self.file_name}"

class Listing(db.Model):
    listing_id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(), index=True, unique=False)
    description = db.Column(db.Text, index=True, unique=False)
    location = db.Column(db.String(), index=True, unique=False)
    date_added = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.resume_id'),
                nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),
                nullable=False)

    def __repr__(self):
        return f"Listing company: {self.company}, location: {self.location}"