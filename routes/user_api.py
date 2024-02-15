from flask import Blueprint, jsonify, request
from models.user import User, UserSchema
from extension import db
from genetic_algorithm.GA import genetic_algorithm, print_menu
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

user_api = Blueprint('user_api',__name__,url_prefix='/api/user')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@user_api.route("/get", methods=["GET"])
def users_list():
    users = User.query.all()
    return users_schema.dump(users)

@user_api.route("/get/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user_details = user.get_user_details()
    return jsonify(user_details)


@user_api.route("/update_username/<id>", methods=["PUT"])
def username_update(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    new_username=request.json["username"]
    user.username = new_username
    db.session.commit()
    return user_schema.jsonify(user)

@user_api.route("/update_age_height_weight/<id>", methods=["PUT"])
def age_height_weight_update(id):
    user = User.query.get(id)
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

@user_api.route("/update_aim/<id>", methods=["PUT"])
def aim_update(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    new_aim=request.json["aim"]
    user.aim = new_aim
    db.session.commit()
    return user_schema.jsonify(user)

@user_api.route("/update_diet/<id>", methods=["PUT"])
def diet_update(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    new_diet=request.json["diet"]
    user.diet = new_diet
    db.session.commit()
    return user_schema.jsonify(user)

@user_api.route("/delete/<id>", methods=["DELETE"])
@jwt_required()
def user_delete(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

@user_api.route('/run_genetic_algorithm', methods=["GET"])
@jwt_required()
def run_genetic_algorithm():
    result = genetic_algorithm()
    return jsonify(result)