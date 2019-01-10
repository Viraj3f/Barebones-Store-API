"""
Contains instances of the API and DB. Mostly boilerplate stuff.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


SERVER_IP = "0.0.0.0"
app = Flask(__name__)
DATABASE_URI = "sqlite:///./database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
