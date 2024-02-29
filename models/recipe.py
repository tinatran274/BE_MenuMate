from extension import db, ma 
from flask import jsonify
from sqlalchemy import ForeignKey
from models.ingredient import Ingredient

class Recipe(db.Model):
    ingredient_id = db.Column(db.Integer, ForeignKey('ingredient.id'), primary_key=True)
    dish_id = db.Column(db.Integer, ForeignKey('dish.id'), primary_key=True)
    unit = db.Column(db.Float)

    def __init__(self, ingredient_id, dish_id, unit):
        self.ingredient_id = ingredient_id
        self.dish_id = dish_id
        self.unit = unit

    def __repr__(self):
        return f'<Recipe {self.ingredient_id} {self.dish_id}>'
    

    def get_unit(self):
        return self.unit
    
    def calculate_grams(self):
        detail_ingr = Ingredient.query.filter_by(id=self.ingredient_id).first()
        if detail_ingr.category == 'Grains':
            return 100*self.unit*20/detail_ingr.glucid
        elif detail_ingr.category == 'Vegetables' or detail_ingr.category == 'Fruits':
            return 80*self.unit
        elif detail_ingr.category == 'Protein':
            return 100*self.unit*7/detail_ingr.protein
        elif detail_ingr.category == 'Dairy':
            return 100*self.unit*100/detail_ingr.canxi
        elif detail_ingr.category == 'Fats and oils':
            return 100*self.unit*5/detail_ingr.lipid
        elif detail_ingr.category == 'Sugar':
            return 5*self.unit
        elif detail_ingr.category == 'Salt and sauces':
            return 1*self.unit
        else:
            return 0
    
    def get_recipe_detail(self):
        grams = self.calculate_grams()
        detail_ingr = Ingredient.query.filter_by(id=self.ingredient_id).first()
        if detail_ingr:
            recipe_details = {
                'ingredient_id': self.ingredient_id,
                'name': detail_ingr.name,
                'unit': self.unit,
                'grams': round(grams, 2),
                'kcal': round(grams*detail_ingr.kcal/100, 2),
                'protein': round(grams*detail_ingr.protein/100, 2),
                'lipid': round(grams*detail_ingr.lipid/100, 2),
                'glucid': round(grams*detail_ingr.glucid/100, 2),
                'canxi': round(grams*detail_ingr.canxi/100, 2),
                'phosphor': round(grams*detail_ingr.phosphor/100, 2),
                'fe': round(grams*detail_ingr.fe/100, 2),
                'vitamin_a': round(grams*detail_ingr.vitamin_a/100, 2),
                'beta_caroten': round(grams*detail_ingr.beta_caroten/100, 2),
                'vitamin_b1': round(grams*detail_ingr.vitamin_b1/100, 2),
                'vitamin_b2': round(grams*detail_ingr.vitamin_b2/100, 2),
                'vitamin_pp': round(grams*detail_ingr.vitamin_pp/100, 2),
                'vitamin_c': round(grams*detail_ingr.vitamin_c/100, 2),
                'category': detail_ingr.category
            }
            return recipe_details
        else:
            return jsonify({'message': 'Ingredient not found'}), 404

        

    
class RecipeSchema(ma.Schema):
    class Meta:
        fields = ('ingredient_id', 'dish_id', 'unit')