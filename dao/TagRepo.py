from dao.models import db
from dao.models import Tag


def create_tag(name):
    tag = Tag(tagname=name)
    db.session.add(tag)
    db.session.commit()


def get_all_tags():
    return Tag.query.all()


def get(tagid):
    return Tag.query.filter_by(tagid=tagid).first()


def delete(tagid):
    db.session.delete(tagid)
    db.session.commit()
