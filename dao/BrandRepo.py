from dao.models import db
from dao.models import Brand


def create_brand(name):
    brand = Brand(brandname=name)
    db.session.add(brand)
    db.session.commit()


def get_all_brands():
    return Brand.query.all()


def get(brandid):
    return Brand.query.filter_by(brandid=brandid).first()


def delete(brandid):
    db.session.delete(brandid)
    db.session.commit()