from extension import db, ma 
from flask import jsonify
from sqlalchemy import ForeignKey

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    age = db.Column(db.Integer)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    gender = db.Column(db.String(100))
    exercise = db.Column(db.String(100))
    aim = db.Column(db.String(100))
    disease_id = db.Column(db.Integer, ForeignKey('disease.id'))

    def __init__(self, username):
        self.username = username
        self.age = 25
        self.height = 160
        self.weight = 50
        self.gender = 'Nữ'
        self.exercise = 'Không vận động'
        self.aim = 'Giảm cân'
        self.disease_id = 3

    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_id(self):
        return self.id
    
    def get_aim(self):
        return self.aim
    
    def get_disease_id(self):
        return self.disease_id

    def calculate_bmi(self):
        bmi = (self.weight / ((self.height / 100) ** 2))
        return bmi

    def calculate_bmr(self):
        if self.gender == 'Nam':
            bmr = int(10 * self.weight + 6.25 * self.height - 5 * self.age + 5)
        elif self.gender == 'Nữ':
            bmr = int(10 * self.weight + 6.25 * self.height - 5 * self.age - 161)
        else:
            return jsonify({'error': 'Invalid gender'})
        return bmr
    
    def calculate_tdee(self):
        tdee_multiplier = 1.2  
        if self.exercise == 'Vận động nhẹ (1-3 ngày/tuần)':
            tdee_multiplier = 1.375
        elif self.exercise == 'Vận động vừa phải (4-5 ngày/tuần)':
            tdee_multiplier = 1.55
        elif self.exercise == 'Vận động nhiều (6-7 ngày/tuần)':
            tdee_multiplier = 1.9
        bmr = self.calculate_bmr()
        tdee = int(bmr * tdee_multiplier)
        return tdee
    
    def get_user_details(self):
        bmi = self.calculate_bmi()
        bmr = self.calculate_bmr()
        tdee = self.calculate_tdee()

        user_details = {
            'user_id': self.id,
            'username': self.username,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'gender': self.gender,
            'exercise': self.exercise,
            'aim': self.aim,
            'bmi': bmi,
            'bmr': bmr,
            'tdee': tdee
        }
        return user_details

    def is_validate_user_data(self):
        if self.age == 0 or self.height == 0 or self.weight == 0:
            return False
        return True
        




    
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'age', 'height', 'weight', 'gender', 'exercise', 'aim')