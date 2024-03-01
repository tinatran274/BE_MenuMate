from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models.account import Account
from models.user import User
from extension import db
from extension import bcrypt


auth = Blueprint('auth',__name__,url_prefix='/api/auth')


@auth.route("/login", methods=["POST"])
def login():
    try:
        email=request.json["email"]
        password=request.json["password"]
        user = Account.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=email)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({'message': 'Đăng nhập thất bại'}), 404
    except Exception as e:
        return jsonify({'message': 'Đăng nhập thất bại.'}), 500

@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_email = get_jwt_identity()
    user_account = Account.query.filter_by(email=current_user_email).first()
    if user_account:
        return jsonify(logged_in_as_user_id=user_account.user_id), 200
    else:
        return jsonify({'message': 'Không tìm thấy người dùng'}), 404
    

@auth.route('/register', methods=['POST'])
def register():
    try:
        email=request.json["email"]
        password=request.json["password"]
        existing_user = Account.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'message': 'Email đã tồn tại. Vui lòng chọn một email khác.'}), 404
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=email)
        db.session.add(new_user)
        db.session.commit()
        new_account = Account(user_id=new_user.id, email=email, password=hashed_password)
        db.session.add(new_account)
        db.session.commit()
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    except Exception as e:
        return jsonify({'message': 'Đăng ký thất bại'}), 500
