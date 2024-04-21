from flask import Blueprint, jsonify, request
from models.user import User, UserSchema
from extension import db
from datetime import datetime
from models.account import Account
from models.suggested_menu import SuggestedMenu
from models.meal import Meal
from flask_jwt_extended import jwt_required, get_jwt_identity
from genetic_algorithm.genetic_algorithm import GeneticAlgorithm
from models.dish import Dish, DishSchema
from sqlalchemy import func

menu_api = Blueprint('menu_api',__name__,url_prefix='/api/menu')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@menu_api.route('/new_genetic_algorithm', methods=["GET"])
@jwt_required()
def new_genetic_algorithm():
    current_user_email = get_jwt_identity()
    user_account = Account.query.filter_by(email=current_user_email).first()
    if not user_account:
        return jsonify({'message': 'Unauthorized'}), 404
    GA = GeneticAlgorithm(6, 0.2, 5, user_account.user_id)
    a = GA.main_genetic_algorithm()
    current_date = datetime.utcnow().date()
    max_num_suggest = (SuggestedMenu.query.with_entities(func.max(SuggestedMenu.num_suggest))
                       .filter(SuggestedMenu.user_id == user_account.user_id, 
                               db.func.date(SuggestedMenu.date_suggest) == current_date).scalar())
    if max_num_suggest:
        new_num_suggest = max_num_suggest + 1
    else:
        new_num_suggest = 1
    new_menu = SuggestedMenu(user_id=user_account.user_id, fitness_score=a['fitness'], 
                             num_suggest=new_num_suggest)
    db.session.add(new_menu)
    db.session.commit()
    for meal_data in a['data']:
        dish_id = meal_data['dish_id']
        dish_order = meal_data['dish_order']
        meal_type = meal_data['meal_type']
        meal = Meal(menu_id=new_menu.id, dish_order=dish_order, dish_id=dish_id, meal_type=meal_type)
        db.session.add(meal)
    db.session.commit()
    return a

@menu_api.route('/get_suggest_menu', methods=["GET"])
@jwt_required()
def get_suggest_menu():
    current_user_email = get_jwt_identity()
    user_account = Account.query.filter_by(email=current_user_email).first()
    if not user_account:
        return jsonify({'message': 'Unauthorized'}), 404
    current_date = datetime.utcnow().date()
    max_suggest_subquery = (db.session.query(func.max(SuggestedMenu.num_suggest))
                            .filter(SuggestedMenu.user_id == user_account.user_id, 
                                    db.func.date(SuggestedMenu.date_suggest) == current_date)
                                    .scalar())
    if max_suggest_subquery:
        result = (db.session.query(SuggestedMenu, Meal, Dish)
                .join(Meal, SuggestedMenu.id == Meal.menu_id)
                .join(Dish, Meal.dish_id == Dish.id)
                .filter(SuggestedMenu.user_id == user_account.user_id, 
                        db.func.date(SuggestedMenu.date_suggest) == current_date, 
                        SuggestedMenu.num_suggest == max_suggest_subquery).all())
        morning_dishs = []
        noon_dishs = []
        dinner_dishs = []
        snack_dishs = []
        for suggested_menu, meal, dish in result:
            if meal.meal_type == "morning":
                morning_dishs.append(dish.to_dict())
            elif meal.meal_type == "noon":
                noon_dishs.append(dish.to_dict())
            elif meal.meal_type == "evening":
                dinner_dishs.append(dish.to_dict())
            else: 
                snack_dishs.append(dish.to_dict())
        return jsonify({
            "morning_dishs": morning_dishs,
            "noon_dishs": noon_dishs,
            "dinner_dishs": dinner_dishs,
            "snacks": snack_dishs,
            "fitness_score": suggested_menu.fitness_score
        })
    else:
        return jsonify({
            "morning_dishs": [],
            "noon_dishs": [],
            "dinner_dishs": [],
            "snacks": [],
            "fitness_score": 0
        })