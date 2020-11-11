"""
Description: Setup the flask application.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder="../static", static_url_path="")
app.secret_key = 'dev'

# enter path to the sqlite file here. A new db is created if one does not exist.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ECosmetics'

db = SQLAlchemy(app)


from dao import models