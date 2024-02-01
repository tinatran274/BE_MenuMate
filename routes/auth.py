from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from models.user import User
from extension import db

auth = Blueprint('auth',__name__,url_prefix='/api/auth')

# Simulate a user database
users = {
    'user1': {'password': 'password1'},
    'user2': {'password': 'password2'}
}

@auth.route("/login", methods=["POST"])
def login():
    email=request.json["email"]
    password=request.json["password"]

    if email in users and users[email]['password'] == password:
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message='Invalid credentials'), 401
    

@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200