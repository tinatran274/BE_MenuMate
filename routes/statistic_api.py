from flask import Blueprint, jsonify, request
from models.user import User, UserSchema
from models.favorite import Favorite
from extension import db
from models.account import Account
from models.statistic import Statistic
from genetic_algorithm.GA import genetic_algorithm, print_menu
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

statistic_api = Blueprint('statistic_api',__name__,url_prefix='/api/statistic')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@statistic_api.route("/get_today", methods=["GET"])
@jwt_required()
def statistic_detail():
    current_user_email = get_jwt_identity()
    user_account = Account.query.filter_by(email=current_user_email).first()
    if not user_account:
        return jsonify({'message': 'Unauthorized'}), 404
    month = request.json["month"]
    day = request.json["day"]
    year = request.json["year"]
    user_statistic = Statistic.query.filter(
        Statistic.user_id == user_account.user_id,
        db.extract('month', Statistic.date_add) == month,
        db.extract('day', Statistic.date_add) == day,
        db.extract('year', Statistic.date_add) == year
    ).all()
    if not user_statistic:
        return jsonify({
            "user_id": user_account.user_id,
            "date_add": f"{day:02d}-{month:02d}-{year}",
            "total_morning_calo": 0,
            "total_noon_calo": 0,
            "total_dinner_calo": 0,
            "total_snack_calo": 0,
            "total_exercise_calo": 0
        }), 200
    results = {
        "user_id": user_account.user_id,
        "date_add": f"{day:02d}-{month:02d}-{year}",
        "total_morning_calo": sum([item.morning_calo for item in user_statistic]),
        "total_noon_calo": sum([item.noon_calo for item in user_statistic]),
        "total_dinner_calo": sum([item.dinner_calo for item in user_statistic]),
        "total_snack_calo": sum([item.snack_calo for item in user_statistic]),
        "total_exercise_calo": sum([item.exercise_calo for item in user_statistic])
    }
    return jsonify(results), 200

@statistic_api.route("/add_morning", methods=["POST"])
@jwt_required()
def add_morning():
    current_user_email = get_jwt_identity()
    user_account = Account.query.filter_by(email=current_user_email).first()
    if not user_account:
        return jsonify({'message': 'Unauthorized'}), 404
    new_morning_calo=request.json["morning_calo"]
    new_statistic = Statistic(user_id=user_account.user_id)
    new_statistic.morning_calo=new_morning_calo
    db.session.add(new_statistic)
    db.session.commit()
    return jsonify({'message': 'add_morning successfully'}), 200

@statistic_api.route("/add_noon", methods=["POST"])
@jwt_required()
def add_noon():
    current_user_email = get_jwt_identity()
    user_account = Account.query.filter_by(email=current_user_email).first()
    if not user_account:
        return jsonify({'message': 'Unauthorized'}), 404
    new_noon_calo=request.json["noon_calo"]
    new_statistic = Statistic(user_id=user_account.user_id)
    new_statistic.noon_calo=new_noon_calo
    db.session.add(new_statistic)
    db.session.commit()
    return jsonify({'message': 'add_morning successfully'}), 200

@statistic_api.route("/add_dinner", methods=["POST"])
@jwt_required()
def add_dinner():
    current_user_email = get_jwt_identity()
    user_account = Account.query.filter_by(email=current_user_email).first()
    if not user_account:
        return jsonify({'message': 'Unauthorized'}), 404
    new_dinner_calo=request.json["dinner_calo"]
    new_statistic = Statistic(user_id=user_account.user_id)
    new_statistic.dinner_calo=new_dinner_calo
    db.session.add(new_statistic)
    db.session.commit()
    return jsonify({'message': 'add_dinner successfully'}), 200

@statistic_api.route("/add_snack", methods=["POST"])
@jwt_required()
def add_snack():
    current_user_email = get_jwt_identity()
    user_account = Account.query.filter_by(email=current_user_email).first()
    if not user_account:
        return jsonify({'message': 'Unauthorized'}), 404
    new_snack_calo=request.json["snack_calo"]
    new_statistic = Statistic(user_id=user_account.user_id)
    new_statistic.snack_calo=new_snack_calo
    db.session.add(new_statistic)
    db.session.commit()
    return jsonify({'message': 'add_snack successfully'}), 200

@statistic_api.route("/add_exercise", methods=["POST"])
@jwt_required()
def add_exercise():
    current_user_email = get_jwt_identity()
    user_account = Account.query.filter_by(email=current_user_email).first()
    if not user_account:
        return jsonify({'message': 'Unauthorized'}), 404
    new_exercise_calo=request.json["exercise_calo"]
    new_statistic = Statistic(user_id=user_account.user_id)
    new_statistic.exercise_calo=new_exercise_calo
    db.session.add(new_statistic)
    db.session.commit()
    return jsonify({'message': 'add_exercise successfully'}), 200



