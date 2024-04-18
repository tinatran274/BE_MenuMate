from flask import Blueprint, jsonify, request
from models.dish import Dish, DishSchema
from models.recipe import Recipe, RecipeSchema
from models.account import Account
from models.favorite import Favorite
from models.user import User, UserSchema
from models.ingredient import Ingredient, IngredientSchema
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from extension import db


dish_api = Blueprint('dish_api',__name__,url_prefix='/api/dish')

dish_schema = DishSchema()
dishs_schema = DishSchema(many=True)
recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)
ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)

@dish_api.route("/get", methods=["GET"])
def dishs_list():
    dishs = Dish.query.all()
    return dishs_schema.dump(dishs)


@dish_api.route('/add_favorite', methods=["POST"])
@jwt_required()
def add_favorite_dish():
    current_user_email = get_jwt_identity()
    user_account = Account.query.filter_by(email=current_user_email).first()
    if not user_account:
        return jsonify({'message': 'Unauthorized'}), 404
    user = User.query.get(user_account.user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    new_favorite_dish_id = request.json["dish_id"]
    dish = Dish.query.get(new_favorite_dish_id)
    if not dish:
        return jsonify({"message": "Món ăn không tồn tại"}), 404
    existing_favorite = (db.session.query(Favorite)
                         .filter_by(dish_id=new_favorite_dish_id, user_id=id).first())
    if existing_favorite:
        return jsonify({'message': 'Món này đã ở trong danh sách yêu thích, bạn có muốn xóa?'}), 201
    else:
        new_favorite = Favorite(id, new_favorite_dish_id)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({'message': 'Thêm thành công'}), 200

@dish_api.route("/get_detail/<id>", methods=["GET"])
@jwt_required()
def dish_detail_user(id):
    current_user_email = get_jwt_identity()
    user_account = Account.query.filter_by(email=current_user_email).first()
    if not user_account:
        return jsonify({'message': 'Unauthorized'}), 404
    dish = Dish.query.get(id)
    favorite_entry = Favorite.query.filter_by(user_id=user_account.user_id, dish_id=id).first()
    if not dish:
        return dish_schema.dump(dish), 200
    return {**dish_schema.dump(dish), **{'is_favorited': bool(favorite_entry)}}

# @dish_api.route("/update/<id>", methods=["PUT"])
# def student_update(id):
#     student = Student.query.get(id)
#     firstname=request.json["firstname"]
#     lastname=request.json["lastname"]
#     student.firstname = firstname
#     student.lastname = lastname
#     db.session.commit()
#     return student_schema.jsonify(student)

# @dish_api.route("/delete/<id>", methods=["DELETE"])
# def student_delete(id):
#     student = Student.query.get(id)
#     db.session.delete(student)
#     db.session.commit()
#     return student_schema.jsonify(student)

@dish_api.route("/recipe/<id>", methods=["GET"])
def ingredient_recipe(id):
    recipes = Recipe.query.filter_by(dish_id=id).all()
    if recipes:
        return recipes_schema.dump(recipes)
    else:
        return jsonify({'message': 'Recipe not found'}), 404
    

@dish_api.route("/detail_recipe/<id>", methods=["GET"])
def detail_ingredient_recipe(id):
    recipes = Recipe.query.filter_by(dish_id=id).all()
    list_ingredient = []
    if recipes:
        for recipe in recipes:
            ingredient_details = recipe.get_recipe_detail()
            list_ingredient.append(ingredient_details)
        return list_ingredient
    else:
        return jsonify({'message': 'Recipe not found'}), 404
    
@dish_api.route("/total_nutrition/<id>", methods=["GET"])
def total_nutrition(id):
    dish = Dish.query.filter_by(id=id).first()
    if dish:
        total_nutrition = dish.to_dict()
        return total_nutrition
    else:
        return jsonify({'message': 'Dish not found'}), 404