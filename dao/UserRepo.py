from dao.models import db, User


def create_user(user):
    db.session.add(user)
    db.session.commit()


def get_user(emailid):
    return User.query.filter_by(email=emailid).first()
