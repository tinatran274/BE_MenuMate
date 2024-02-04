from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from routes.student_api import student_api
from routes.user_api import user_api
from routes.auth import auth
from extension import db
from datetime import timedelta


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://admin:123456789@database.crw4qiio2s1e.ap-southeast-1.rds.amazonaws.com/database1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'QWERTY'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

@app.route('/')
def home():
    return 'Hello, World!'

db.init_app(app)
app.register_blueprint(student_api)
app.register_blueprint(auth)
app.register_blueprint(user_api)

jwt = JWTManager(app)
                 

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(host='0.0.0.0', port='5000')