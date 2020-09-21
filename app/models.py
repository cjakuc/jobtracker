from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    resumes = db.relationship('Resume', backref='user', lazy=True)
    listings = db.relationship('Listing', backref='user', lazy=True)
    cover_letters = db.relationship('CoverLetter', backref='user', lazy=True)

    def __repr__(self):
        return f"User: {self.username}"

    # Functions to set and check the password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(64), index=True, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
              nullable=False)
    listings = db.relationship('Listing', backref='resume', lazy=True)

    def __repr__(self):
        return f"{self.file_name}"

class CoverLetter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(64), index=True, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
              nullable=False)
    listings = db.relationship('Listing', backref='cover_letter', lazy=True)

    def __repr__(self):
        return f"{self.file_name}"

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(), index=True, unique=False)
    title = db.Column(db.String(), index=True, unique=False)
    description = db.Column(db.Text, index=False, unique=False)
    location = db.Column(db.String(), index=True, unique=False)
    date_added = db.Column(db.DateTime, index=True, default=datetime.today())
    status = db.Column(db.String(), index=False, unique=False,
                       default="No Response", nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'),
                nullable=False)
    cl_id = db.Column(db.Integer, db.ForeignKey('cover_letter.id'),
                nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                nullable=False)

    def __repr__(self):
        return f"Date Applied: {self.date_added}, Role: {self.title}, Company: {self.company}, Location: {self.location}"

# Function to load a user to help Flask-Login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))