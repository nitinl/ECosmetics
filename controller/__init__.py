"""
Description: Setup the flask application.
"""

from flask import Flask
from flask_migrate import Migrate

from dao.models import db

app = Flask(__name__, static_folder="../static", static_url_path="")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ECosmetics'

migrate = Migrate(app, db)
db.init_app(app)

db.app = app

from controller import CosmeticAPIController
from controller import AccessExternalAPIController

from dao import models

if __name__ == '__main__':
    db.create_all()
    db.session.commit()
