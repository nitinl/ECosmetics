import datetime

from flask import request, make_response, jsonify
from controller import app
from dao import UserRepo
from dao.models import User
from flask_jwt_extended import create_access_token

"""
API call for signup
"""


@app.route('/signup', methods=['POST'])
def signup():
    body = request.get_json()
    user = User(**body)
    user.hash_password()
    UserRepo.create_user(user)
    return make_response(jsonify(response='User added successfully'), 201)

"""
API call to login and give the access token as output
"""


@app.route('/login', methods=['POST'])
def login():
    user = UserRepo.get_user(request.get_json().get('email'))
    authorized = user.check_password(request.get_json().get('password'))
    if not authorized:
        return {'error': 'Email or password invalid'}, 401

    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity=str(user.email), expires_delta=expires)
    return {'token': access_token}, 200
