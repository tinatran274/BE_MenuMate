from extension import db, ma 
from sqlalchemy import ForeignKey

class CannotEat(db.Model):
    disease_id = db.Column(db.Integer, ForeignKey('disease.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, ForeignKey('ingredient.id'), primary_key=True)

    def __init__(self, disease_id, ingredient_id):
        self.disease_id = disease_id
        self.ingredient_id = ingredient_id

    def __repr__(self):
        return f'<CannotEat {self.disease_id} {self.ingredient_id}>'