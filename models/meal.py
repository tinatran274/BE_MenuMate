from datetime import datetime
from extension import db, ma 
from sqlalchemy import ForeignKey

class Meal(db.Model):
    menu_id = db.Column(db.Integer, ForeignKey('suggested_menu.id'), primary_key=True)
    dish_order = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, ForeignKey('dish.id'), nullable=False)
    meal_type = db.Column(db.String(255), primary_key=True)

    def __init__(self, menu_id, dish_order, dish_id, meal_type):
        self.menu_id = menu_id
        self.dish_order = dish_order
        self.dish_id = dish_id
        self.meal_type = meal_type

    def __repr__(self):
        return f'<Meal {self.menu_id} {self.dish_order}>'