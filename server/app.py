"""
Contains instances of the API and DB.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


SERVER_IP = "0.0.0.0"
DATABASE_URI = "sqlite:///./database.db"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
