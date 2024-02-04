from flask import Blueprint, jsonify, request
from models.user import User, UserSchema
from extension import db

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
def user_update(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    new_username=request.json["username"]
    user.username = new_username
    db.session.commit()
    return user_schema.jsonify(user)

@user_api.route("/delete/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)