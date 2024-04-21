from flask import Flask
from flask_jwt_extended import JWTManager
from routes.student_api import student_api
from routes.user_api import user_api
from routes.dish_api import dish_api
from routes.ingredient_api import ingredient_api
from routes.statistic_api import statistic_api
from routes.menu_api import menu_api
from routes.auth import auth
from models.ingredient import Ingredient
from models.dish import Dish
from models.recipe import Recipe
from models.disease import Disease
from models.cannot_eat import CannotEat
from models.statistic import Statistic
from extension import db
import pandas as pd
from datetime import timedelta



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:123456@localhost/menu_mate'
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
app.register_blueprint(dish_api)
app.register_blueprint(ingredient_api)
app.register_blueprint(statistic_api)
app.register_blueprint(menu_api)

jwt = JWTManager(app)
                 
def init_ingredient_data():
    print('Initializing ingredient data')
    df = pd.read_csv('ingredient_data.csv')
    for index, row in df.iterrows():
        ingredient = Ingredient(
            name=row[0],
            removal=row[1],
            kcal=row[2],
            protein=row[3],
            lipid=row[4],
            glucid=row[5],
            canxi=row[6],
            phosphor=row[7],
            fe=row[8],
            vitamin_a=row[9],
            beta_caroten=row[10],
            vitamin_b1=row[11],
            vitamin_b2=row[12],
            vitamin_pp=row[13],
            vitamin_c=row[14],
            category=row[15]
        )
        db.session.add(ingredient)
    db.session.commit()

def init_dish_data():
    print('Initializing dish data')
    df = pd.read_csv('dish_data.csv')
    for index, row in df.iterrows():
        dish = Dish(
            name=row[0],
            main_category=row[1]
        )
        db.session.add(dish)
    db.session.commit()

def init_recipe_data():
    print('Initializing recipe data')
    df = pd.read_csv('recipe_data.csv')
    for index, row in df.iterrows():
        recipe = Recipe(
            ingredient_id=row[0],
            dish_id=row[1],
            unit=row[2]
        )
        db.session.add(recipe)
    db.session.commit()


def init_disease_data():
    print('Initializing disease data')
    df = pd.read_csv('disease_data.csv')
    for index, row in df.iterrows():
        disease = Disease(
            disease_name=row[0]
        )
        db.session.add(disease)
    db.session.commit()

def init_cannot_eat_data():
    print('Initializing cannot_eat data')
    df = pd.read_csv('cannot_eat_data.csv')
    for index, row in df.iterrows():
        cannot_eat = CannotEat(
            disease_id=row[0],
            ingredient_id=row[1],
        )
        db.session.add(cannot_eat)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not Ingredient.query.first():
            init_ingredient_data()
        if not Dish.query.first():
            init_dish_data()
        if not Recipe.query.first():
            init_recipe_data()
        if not Disease.query.first():
            init_disease_data()
        if not CannotEat.query.first():
            init_cannot_eat_data()
        
        app.run(host='0.0.0.0', port='5000')