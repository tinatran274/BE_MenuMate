from flask import Blueprint, jsonify, request
from models.dish import Dish, DishSchema
from models.recipe import Recipe, RecipeSchema
from models.ingredient import Ingredient, IngredientSchema
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

# @dish_api.route("/create", methods=["POST"])
# def student_create():
#     firstname=request.json["firstname"]
#     lastname=request.json["lastname"]
#     new_student = Dish(firstname, lastname)
#     db.session.add(new_student)
#     db.session.commit()
#     return dishs_schema.jsonify(new_student)

@dish_api.route("/get/<id>", methods=["GET"])
def dish_detail(id):
    dish = Dish.query.get(id)
    return dish_schema.dump(dish)

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