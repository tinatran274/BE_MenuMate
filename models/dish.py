from extension import db, ma 
from flask import jsonify
from models.recipe import Recipe, RecipeSchema

class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    main_category = db.Column(db.String(255), nullable=False)

    def __init__(self, name,  main_category):
        self.name = name
        self.main_category = main_category

    def __repr__(self):
        return f'<Dish {self.name}>'
    
    
    def to_dict(self):
        recipes = Recipe.query.filter_by(dish_id=self.id).all()
        total_kcal = 0
        total_protein = 0
        total_glucid = 0
        total_lipid = 0
        if recipes:
            for recipe in recipes:
                ingredient_details = recipe.get_recipe_detail()
                total_kcal  += ingredient_details['kcal']
                total_protein  += ingredient_details['protein']
                total_glucid  += ingredient_details['glucid']
                total_lipid  += ingredient_details['lipid']
            total_nutrition = {
                "id": self.id,
                "name": self.name,
                "main_category": self.main_category,
                "total_kcal" : round(total_kcal, 2),
                "total_protein": round(total_protein, 2),
                "total_glucid": round(total_glucid, 2),
                "total_lipid": round(total_lipid, 2)
            }
            return total_nutrition
        else:
            return {
                "id": self.id,
                "name": self.name,
                "main_category": self.main_category,
                "total_kcal" : 0,
                "total_protein": 0,
                "total_glucid": 0,
                "total_lipid": 0
            }

class DishSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'main_category')