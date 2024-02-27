from flask import Blueprint, jsonify, request
from models.ingredient import Ingredient, IngredientSchema
from extension import db

ingredient_api = Blueprint('ingredient_api',__name__,url_prefix='/api/ingredient')

ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)


@ingredient_api.route("/get", methods=["GET"])
def ingredients_list():
    ingredients = Ingredient.query.all()
    return ingredients_schema.dump(ingredients)

# @ingredient_api.route("/create", methods=["POST"])
# def student_create():
#     firstname=request.json["firstname"]
#     lastname=request.json["lastname"]
#     new_student = Dish(firstname, lastname)
#     db.session.add(new_student)
#     db.session.commit()
#     return dishs_schema.jsonify(new_student)

@ingredient_api.route("/get/<id>", methods=["GET"])
def ingredient_dish_detail(id):
    ingredient = Ingredient.query.get(id)
    return ingredient_schema.dump(ingredient)

# @ingredient_api.route("/update/<id>", methods=["PUT"])
# def student_update(id):
#     student = Student.query.get(id)
#     firstname=request.json["firstname"]
#     lastname=request.json["lastname"]
#     student.firstname = firstname
#     student.lastname = lastname
#     db.session.commit()
#     return student_schema.jsonify(student)

# @ingredient_api.route("/delete/<id>", methods=["DELETE"])
# def student_delete(id):
#     student = Student.query.get(id)
#     db.session.delete(student)
#     db.session.commit()
#     return student_schema.jsonify(student)