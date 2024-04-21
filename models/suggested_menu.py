from datetime import datetime
from extension import db, ma 
from sqlalchemy import ForeignKey

class SuggestedMenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    date_suggest = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    fitness_score = db.Column(db.Integer)
    num_suggest = db.Column(db.Integer)

    def __init__(self, user_id, num_suggest, fitness_score):
        self.user_id = user_id
        self.num_suggest = num_suggest
        self.fitness_score = fitness_score

    def __repr__(self):
        return f'<SuggestedMenu {self.id} {self.user_id}>'