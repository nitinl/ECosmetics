"""
Description: Setup the flask application.
"""

from flask import Flask
from flask_migrate import Migrate
from dao.models import db
from sqlalchemy.engine import Engine
from sqlalchemy import event

app = Flask(__name__, static_folder="../static", static_url_path="")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ECosmetics'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)
db.app = app


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


if __name__ == '__main__':
    db.create_all()
    db.session.commit()
