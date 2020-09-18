from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Create the app
app = Flask(__name__)
# Configure the app with the attributes of the Config class
app.config.from_object(Config)

# Add the login manage to the app
login = LoginManager(app)
# Tell Flask what the view function is that handles logins
## This allows Flask-Login to force users to sign in
## before viewing certain pages (using @login_required in routes.py)
login.login_view = 'login'

# Create the DB connection and migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models