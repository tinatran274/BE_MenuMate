from extension import db, ma 
from datetime import datetime
from sqlalchemy import ForeignKey

class Statistic(db.Model):
    user_id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)
    date_add = db.Column(db.DateTime, default=datetime.utcnow, primary_key=True)
    morning_calo = db.Column(db.Integer)
    noon_calo = db.Column(db.Integer)
    dinner_calo = db.Column(db.Integer)
    snack_calo = db.Column(db.Integer)
    exercise_calo = db.Column(db.Integer)
    

    def __init__(self, user_id):
        self.user_id = user_id
        self.morning_calo = 0
        self.noon_calo = 0
        self.dinner_calo = 0
        self.snack_calo = 0
        self.exercise_calo = 0

    def get_user_statistic_details(self):
        user_details = {
            'user_id': self.user_id,
            'morning_calo': self.morning_calo,
            'noon_calo': self.noon_calo,
            'dinner_calo': self.dinner_calo,
            'snack_calo': self.snack_calo,
            'exercise_calo': self.exercise_calo,
        }
        return user_details


    def __repr__(self):
        return f'<Statistic {self.user_id}>'