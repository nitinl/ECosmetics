from dao.models import db
from dao.models import Category


def create_category(categoryname):
    category = Category(categoryname=categoryname)
    db.session.add(category)
    db.session.commit()


def get_all_categories():
    return Category.query.all()


def get(categoryid):
    return Category.query.filter_by(categoryid=categoryid).first()


def delete(categoryid):
    db.session.delete(categoryid)
    db.session.commit()