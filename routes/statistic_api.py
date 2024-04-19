from flask import Blueprint, jsonify, request
from models.user import User, UserSchema
from models.favorite import Favorite
from extension import db
from datetime import datetime, timedelta
from models.account import Account
from models.statistic import Statistic
from genetic_algorithm.GA import genetic_algorithm, print_menu
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

statistic_api = Blueprint('statistic_api',__name__,url_prefix='/api/statistic')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

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

@statistic_api.route("/sevendays_statistic", methods=["GET"])
@jwt_required()
def sevendays_statistic():
    current_user_email = get_jwt_identity()
    user_account = Account.query.filter_by(email=current_user_email).first()
    if not user_account:
        return jsonify({'message': 'Unauthorized'}), 404
    num_days = int(request.args.get('days', 7))
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=num_days-1)
    statistics_by_day = []
    for i in range(num_days):
        current_date = start_date + timedelta(days=i)
        user_statistic = Statistic.query.filter(
            Statistic.user_id == user_account.user_id,
            db.func.date(Statistic.date_add) == current_date
        ).all()
        daily_stats = {
            "date": current_date.isoformat(),
            "total_morning_calo": 0,
            "total_noon_calo": 0,
            "total_dinner_calo": 0,
            "total_snack_calo": 0,
            "total_exercise_calo": 0,
            "total_calo": 0
        }
        if user_statistic:
            daily_stats["total_morning_calo"] = sum(item.morning_calo for item in user_statistic)
            daily_stats["total_noon_calo"] = sum(item.noon_calo for item in user_statistic)
            daily_stats["total_dinner_calo"] = sum(item.dinner_calo for item in user_statistic)
            daily_stats["total_snack_calo"] = sum(item.snack_calo for item in user_statistic)
            daily_stats["total_exercise_calo"] = sum(item.exercise_calo for item in user_statistic)
            daily_stats["total_calo"] = (
                daily_stats["total_morning_calo"] + daily_stats["total_noon_calo"] +
                daily_stats["total_dinner_calo"] + daily_stats["total_snack_calo"] -
                daily_stats["total_exercise_calo"]
            )
        statistics_by_day.append(daily_stats)
    return jsonify(statistics_by_day), 200


