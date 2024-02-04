from extension import db, ma 
from datetime import datetime
from sqlalchemy import ForeignKey

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, email, password):
        self.user_id = user_id
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<Account {self.email}>'