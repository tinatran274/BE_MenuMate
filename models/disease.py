from extension import db, ma 
from flask import jsonify
import random

class Disease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disease_name = db.Column(db.String(255), nullable=False)

    def __init__(self, disease_name):
        self.disease_name = disease_name

    def __repr__(self):
        return f'<Disease {self.disease_name}>'
    
    def get_id(self):
        return self.id
    
    def get_disease_name(self):
        return self.disease_name
    
    

    
    # def to_dict(self):
    #     recipes = Recipe.query.filter_by(dish_id=self.id).all()
    #     total_kcal = 0
    #     if recipes:
    #         for recipe in recipes:
    #             ingredient_details = recipe.get_recipe_detail()
    #             total_kcal  += ingredient_details['kcal']
    #         total_nutrition = {
    #             "id": self.id,
    #             "name": self.name,
    #             "main_category": self.main_category,
    #             "total_kcal" : round(total_kcal, 2),
    #         }
    #         return total_nutrition
    #     else:
    #         return {
    #             "id": self.id,
    #             "name": self.name,
    #             "main_category": self.main_category,
    #             "total_kcal" : 0,
    #         }

class DiseaseSchema(ma.Schema):
    class Meta:
        fields = ('id', 'disease_name')