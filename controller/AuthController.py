import datetime

from flask import request, make_response, jsonify
from controller import app
from dao import UserRepo
from dao.models import User
from flask_jwt_extended import create_access_token

"""
API call for user signup
"""


@app.route('/signup', methods=['POST'])
def signup():
    body = request.get_json()
    user = User(**body)
    if len(body.get("password")) > 8:
        user.hash_password()
    else:
        return make_response(jsonify(response='Password must contain at least 8 characters'), 400)
    UserRepo.create_user(user)
    return make_response(jsonify(response='User added successfully'), 201)

"""
API call to login and give the access token as output for user
"""


@app.route('/login', methods=['POST'])
def login():
    """
        @return: Returns the access token which is used for accessing other API calls
    """
    user = UserRepo.get_user(request.get_json().get('email'))
    if user is not None:
        authorized = user.check_password(request.get_json().get('password'))
        if not authorized:
            return {'error': 'Email or password invalid'}, 401
    else:
        return {'error': 'No such User. Please signup to proceed further'}, 401

    expires = datetime.timedelta(days=3)
    access_token = create_access_token(identity=str(user.email), expires_delta=expires)
    return make_response(jsonify(token=access_token), 200)
