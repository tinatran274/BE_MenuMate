from extension import db, ma 
from sqlalchemy import ForeignKey

class Favorite(db.Model):
    user_id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)
    dish_id = db.Column(db.Integer, ForeignKey('dish.id'), primary_key=True)

    def __init__(self, user_id, dish_id):
        self.user_id = user_id
        self.dish_id = dish_id

    def __repr__(self):
        return f'<Favorite {self.user_id} {self.dish_id}>'