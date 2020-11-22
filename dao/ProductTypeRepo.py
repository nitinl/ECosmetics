from dao.models import db
from dao.models import ProductType


def create_producttype(prodtypename):
    producttype = ProductType(typename=prodtypename)
    db.session.add(producttype)
    db.session.commit()


def get_all_producttypes():
    return ProductType.query.all()


def get(typeid):
    return ProductType.query.filter_by(typeid=typeid).first()


def delete(typeid):
    db.session.delete(typeid)
    db.session.commit()
