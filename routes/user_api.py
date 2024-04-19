from flask import Blueprint, jsonify, request
from models.user import User, UserSchema
from models.favorite import Favorite
from extension import db
from datetime import datetime
from models.statistic import Statistic
from models.account import Account
from genetic_algorithm.GA import genetic_algorithm, print_menu
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from genetic_algorithm.genetic_algorithm import GeneticAlgorithm
from models.dish import Dish, DishSchema
from ultralytics import YOLO

user_api = Blueprint('user_api',__name__,url_prefix='/api/user')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
dish_schema = DishSchema()
dishs_schema = DishSchema(many=True)

# @user_api.route("/get", methods=["GET"])
# def users_list():
#     users = User.query.all()
#     return users_schema.dump(users)

@user_api.route("/get", methods=["GET"])
@jwt_required()
def user_detail():
    current_user_email = get_jwt_identity()
    user_account = Account.query.filter_by(email=current_user_email).first()
    if not user_account:
        return jsonify({'message': 'Unauthorized'}), 404
    user = User.query.get(user_account.user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user_details = user.get_user_details()
    return jsonify(user_details)


@user_api.route("/update_username", methods=["PUT"])
@jwt_required()
def username_update():
    current_user_email = get_jwt_identity()
    user_account = Account.query.filter_by(email=current_user_email).first()
    if not user_account:
        return jsonify({'message': 'Unauthorized'}), 404
    user = User.query.get(user_account.user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    new_username=request.json["username"]
    user.username = new_username
    db.session.commit()
    return user_schema.jsonify(user)

@user_api.route("/update_age_height_weight", methods=["PUT"])
@jwt_required()
def age_height_weight_update():
    current_user_email = get_jwt_identity()
    user_account = Account.query.filter_by(email=current_user_email).first()
    if not user_account:
        return jsonify({'message': 'Unauthorized'}), 404
    user = User.query.get(user_account.user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    new_age=request.json["age"]
    new_height=request.json["height"]
    new_weight=request.json["weight"]
    user.age = new_age
    user.height = new_height
    user.weight = new_weight
    db.session.commit()
    return user_schema.jsonify(user)

@user_api.route("/update_aim", methods=["PUT"])
@jwt_required()
def aim_update():
    current_user_email = get_jwt_identity()
    user_account = Account.query.filter_by(email=current_user_email).first()
    if not user_account:
        return jsonify({'message': 'Unauthorized'}), 404
    user = User.query.get(user_account.user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    new_aim=request.json["aim"]
    user.aim = new_aim
    db.session.commit()
    return user_schema.jsonify(user)

@user_api.route("/update_gender", methods=["PUT"])
@jwt_required()
def gender_update():
    current_user_email = get_jwt_identity()
    user_account = Account.query.filter_by(email=current_user_email).first()
    if not user_account:
        return jsonify({'message': 'Unauthorized'}), 404
    user = User.query.get(user_account.user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    new_gender=request.json["gender"]
    user.gender = new_gender
    db.session.commit()
    return user_schema.jsonify(user)

@user_api.route("/update_exercise", methods=["PUT"])
@jwt_required()
def exercise_update():
    current_user_email = get_jwt_identity()
    user_account = Account.query.filter_by(email=current_user_email).first()
    if not user_account:
        return jsonify({'msg': 'Unauthorized'}), 404
    user = User.query.get(user_account.user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    new_exercise=request.json["exercise"]
    user.exercise = new_exercise
    db.session.commit()
    return user_schema.jsonify(user)

@user_api.route("/delete", methods=["DELETE"])
@jwt_required()
def user_delete():
    current_user_email = get_jwt_identity()
    user_account = Account.query.filter_by(email=current_user_email).first()
    if not user_account:
        return jsonify({'message': 'Unauthorized'}), 404
    user = User.query.get(user_account.user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

@user_api.route('/run_genetic_algorithm', methods=["GET"])
@jwt_required()
def run_genetic_algorithm():
    result = genetic_algorithm()
    return jsonify("")

@user_api.route('/new_genetic_algorithm', methods=["GET"])
@jwt_required()
def new_genetic_algorithm():
    current_user_email = get_jwt_identity()
    user_account = Account.query.filter_by(email=current_user_email).first()
    if not user_account:
        return jsonify({'message': 'Unauthorized'}), 404
    user = User.query.get(user_account.user_id)
    if not user:
        return jsonify({'message': 'Không tồn tại người dùng này'}), 404
    if not user.is_validate_user_data():
        return jsonify({'message': 'Người dùng chưa hoàn thành thông tin cơ bản.'}), 404
    GA = GeneticAlgorithm(6, 0.2, 5, id)
    a = GA.main_genetic_algorithm()
    return a

@user_api.route('/detect_ingredient', methods=['POST'])
def detect_ingredient():
    model = YOLO('yolov9c.pt')
    model.info()
    results = model.train(data='coco8.yaml', epochs=100, imgsz=640)
    results = model('path/to/bus.jpg')

@user_api.route("/get_today", methods=['GET'])
@jwt_required()
def get_today():
    current_user_email = get_jwt_identity()
    user_account = Account.query.filter_by(email=current_user_email).first()
    if not user_account:
        return jsonify({'message': 'Unauthorized'}), 404
    current_date = datetime.now().date()
    day, month, year = current_date.day, current_date.month, current_date.year
    
    user_statistic = Statistic.query.filter(
        Statistic.user_id == user_account.user_id,
        db.extract('day', Statistic.date_add) == day,
        db.extract('month', Statistic.date_add) == month,
        db.extract('year', Statistic.date_add) == year
    ).all()
    if not user_statistic:
        return jsonify({
            "user_id": user_account.user_id,
            "date_add": current_date.strftime("%d-%m-%Y"), 
            "total_morning_calo": 0,
            "total_noon_calo": 0,
            "total_dinner_calo": 0,
            "total_snack_calo": 0,
            "total_exercise_calo": 0
        }), 200
    results = {
        "user_id": user_account.user_id,
        "date_add": current_date.strftime("%d-%m-%Y"),
        "total_morning_calo": sum([item.morning_calo for item in user_statistic]),
        "total_noon_calo": sum([item.noon_calo for item in user_statistic]),
        "total_dinner_calo": sum([item.dinner_calo for item in user_statistic]),
        "total_snack_calo": sum([item.snack_calo for item in user_statistic]),
        "total_exercise_calo": sum([item.exercise_calo for item in user_statistic])
    }
    return jsonify(results), 200