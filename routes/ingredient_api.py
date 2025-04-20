from flask import Blueprint, jsonify, request
from models.ingredient import Ingredient, IngredientSchema
from extension import db
from models.dish import Dish, DishSchema
from models.recipe import Recipe, RecipeSchema
from sqlalchemy import func

ingredient_api = Blueprint('ingredient_api',__name__,url_prefix='/api/ingredient')

ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)


@ingredient_api.route("/get_all", methods=["GET"])
def ingredients_list_all():
    ingredients = Ingredient.query.all()
    return ingredients_schema.dump(ingredients)

@ingredient_api.route("/get", methods=["GET"])
def ingredients_list():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    category = request.args.get('category', '').strip()
    offset = (page - 1) * page_size
    if category:
        total_ingredients_by_category = (
            db.session.query(Ingredient.category, func.count())
            .filter(Ingredient.category == category)
            .group_by(Ingredient.category)
            .all()
        )
        total_ingredients = total_ingredients_by_category[0][1] if total_ingredients_by_category else 0
        ingredients = Ingredient.query.filter_by(category=category).offset(offset).limit(page_size).all()
    else:
        total_ingredients = Ingredient.query.count()
        ingredients = Ingredient.query.offset(offset).limit(page_size).all()
    serialized_ingredients = ingredients_schema.dump(ingredients)
    total_pages = (total_ingredients + page_size - 1) // page_size
    pagination_metadata = {
        "current_page": page,
        "page_size": page_size,
        "total_items": total_ingredients,
        "total_pages": total_pages
    }
    response = {
        "data": serialized_ingredients,
        "pagination": pagination_metadata
    }
    return jsonify(response), 200

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

@ingredient_api.route("/get_dish/<id>", methods=["GET"])
def dishs_list(id):
    dishs = db.session.query(Dish).join(Recipe, Dish.id == Recipe.dish_id).filter(
        Recipe.ingredient_id == id
    ).all()
    serialized_dishs = []
    if dishs:
        for dish in dishs:
            total_nutrition = dish.to_dict()
            serialized_dishs.append(total_nutrition)
    return jsonify(serialized_dishs), 200

@ingredient_api.route("/detect", methods=["PUT"])
def detect_ingredient():

    

    
    return True


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


