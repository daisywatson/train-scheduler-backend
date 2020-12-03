import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash

from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user


users = Blueprint('users', 'user')

@users.route('/', methods=['GET'])
def test_user_resources():
    return "user resource works"

@users.route('/register', methods=['POST'])
def register():
    payload = request.get_json()
    print(payload)

    payload['username'] = payload['username'].lower()

    try:
        models.User.get(models.User.username == payload['username'])
        return jsonify(
            data={},
            message="A user with that username already exists",
            status=401
        ), 401
    except models.DoesNotExist:
        pw_hash = generate_password_hash(payload['password'])
        created_user = models.User.create(
            username=payload['username'],
            password=pw_hash
        )
        print(created_user)
        created_user_dict = model_to_dict(created_user)
        print(created_user_dict)
        login_user(created_user)
        created_user_dict.pop('password')
        return jsonify(
            data=created_user_dict,
            message=f"Successfully registered user with {created_user_dict['username']}",
            status=201
        ), 201

@users.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    payload['username'] = payload['username'].lower()

    try:
        user = models.User.get(models.User.username == payload['username'])

        # if user exists:
        user_dict = model_to_dict(user)
        # check the password
        password_is_good = check_password_hash(user_dict['password'],
        payload['password'])

        if(password_is_good):
            # log in
            login_user(user)
            user_dict.pop('password')

            return jsonify(
                data=user_dict,
                message=f"Successfully logged in {user_dict['username']}",
                status=200
            ), 200
        else:
            return jsonify(
                data={},
                message="Username or password is incorrect",
                status=401
            ), 401
    except models.DoesNotExist:
        return jsonify(
            data={},
            message="Username or password is incorrect",
            status=401
        ), 401

@users.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify(
        data={},
        message="successful logout",
        status=200
    ), 200
