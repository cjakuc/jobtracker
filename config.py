import os
from dotenv import load_dotenv


class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY", default="OOPS") or "my_secret"
    SQLALCHEMY_DATABASE_URI = os.getenv("DBURL", default="OOPS")
    SQLALCHEMY_TRACK_MODIFICATIONS = False