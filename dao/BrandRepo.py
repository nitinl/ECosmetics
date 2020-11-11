from controller import db
from dao.models import Brand


def create_brand(name):
    brand = Brand(brandname=name)
    db.session.add(brand)
    db.session.commit()


def get_all_brands():
    brands = Brand.query.all()
    return brands


def get(brandid):
    return Brand.query.filter_by(brandid=brandid).first()
