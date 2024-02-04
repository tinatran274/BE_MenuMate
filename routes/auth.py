from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models.account import Account
from models.user import User
from extension import db
from extension import bcrypt


auth = Blueprint('auth',__name__,url_prefix='/api/auth')


@auth.route("/login", methods=["POST"])
def login():
    email=request.json["email"]
    password=request.json["password"]

    user = Account.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message='Invalid credentials'), 401
    

@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@auth.route('/register', methods=['POST'])
def register():
    email=request.json["email"]
    password=request.json["password"]

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=email)
    db.session.add(new_user)
    db.session.commit()
    new_account = Account(user_id=new_user.id, email=email, password=hashed_password)
    db.session.add(new_account)
    db.session.commit()

    return jsonify(message='User registered successfully'), 201