from extension import db, ma 
from sqlalchemy import ForeignKey

class Favorite(db.Model):
    user_id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)
    dish_id = db.Column(db.Integer, ForeignKey('dish.id'), primary_key=True)
    value = db.Column(db.Integer)

    def __init__(self, user_id, dish_id, value):
        self.user_id = user_id
        self.dish_id = dish_id
        self.value = value

    def __repr__(self):
        return f'<Favorite {self.user_id} {self.dish_id} {self.value}>'

    def get_value(self):
        return self.value