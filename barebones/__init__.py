"""
Contains instances of the API and DB. Mostly boilerplate stuff.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


SERVER_IP = "0.0.0.0"
app = Flask(__name__)
DATABASE_URI = "sqlite:///./database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "my-secret-key-do-not-do-this-in-prod-lol"
db = SQLAlchemy(app)

# Circular import... because Flask
import barebones.api
import barebones.model
