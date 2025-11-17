# config.py
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "change-this-to-a-better-secret"  # for sessions/forms later
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "lilybloom.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
