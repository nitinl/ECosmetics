from dao.models import db
from dao.models import Color


def create_color(colorname):
    color = Color(colorname=colorname)
    db.session.add(color)
    db.session.commit()


def get_all_colors():
    return Color.query.all()


def get(colorid):
    return Color.query.filter_by(colorid=colorid).first()


def delete(colorid):
    db.session.delete(colorid)
    db.session.commit()
