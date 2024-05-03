import random
from models.dish import Dish, DishSchema
from models.recipe import Recipe, RecipeSchema
from models.user import User, UserSchema
from models.ingredient import Ingredient
from models.disease import Disease
from models.cannot_eat import CannotEat
from models.favorite import Favorite

from extension import db, ma 

class MenuIndividual:
    MEAL_CATEGORIES = {'morning': 4, 'noon': 4, 'evening': 4, 'snack': 1}
    NUM_GENES = sum(MEAL_CATEGORIES.values())

    def __init__(self, uid, list_dish=None):
        self.uid = uid
        if list_dish is None:
            self.menu = [self.random_dish() for _ in range(self.NUM_GENES)]
        else:
            self.menu = list_dish

        self.fitness = self.calculate_fitness_score()

    def get_fitness(self):
        return self.fitness

    def random_num(self, start, end):
        range_val = (end - start) + 1
        random_int = start + random.randint(0, range_val - 1)
        return random_int

    def random_dish(self):
        dishs = Dish.query.all()
        length_data = len(dishs); 
        random_index = self.random_num(0, length_data-1); 
        return dishs[random_index]; 

    def to_dict(self):
        menu = {}
        temp_menu = self.menu
        category_info = []
        for category, count in self.MEAL_CATEGORIES.items():
            category_dishes = temp_menu[:count]
            for index, dish in enumerate(category_dishes):
                dish_info = {
                    'dish_id': dish.get_id(),
                    'dish_order': index + 1,
                    'meal_type': category
                }
                category_info.append(dish_info)
            temp_menu = temp_menu[count:]
        menu['fitness'] = self.fitness
        menu['data'] = category_info
        return menu
    
    def calculate_food_diversity_score(self):
        temp_menu = self.menu
        unique_category = len(set(dish.get_name() for dish in temp_menu))
        return unique_category * 5
    
    def calculate_food_group_diversity_score(self):
        num_dish_accept = 0
        temp_menu = self.menu
        morning_require = {'Grains', 'Protein', 'Fruits', 'Dairy'}
        noon_evening_require = {'Grains', 'Protein', 'Fruits', 'Vegetables'}
        snack_require = {'Fruits', 'Dairy'}
        for category, count in self.MEAL_CATEGORIES.items():
            category_dishes = temp_menu[:count]
            category_group = set(dish.get_main_category() for dish in category_dishes)
            if category == 'morning':
                matching_num = len(category_group & morning_require)
                num_dish_accept += matching_num
            elif category == 'noon' or category == 'evening':
                matching_num = len(category_group & noon_evening_require)
                num_dish_accept += matching_num
            elif category == 'snack':
                matching_num = len(category_group & snack_require)
                num_dish_accept += matching_num
            temp_menu = temp_menu[count:]
        return num_dish_accept * 5
    

    def calculate_VHEI_calo_score(self):
        vegetable_unit = fruit_unit = grain_unit = protein_unit = fat_n_oil_unit = 0
        dairy_unit = sugar_unit = salt_n_sauce_unit = total_kcal = 0
        for dish in self.menu:
            result = (
                db.session.query(Dish.id, Recipe.unit, Ingredient.kcal, Ingredient.glucid,
                                Ingredient.protein, Ingredient.canxi, Ingredient.lipid,
                                Ingredient.category)
                .join(Recipe, Dish.id == Recipe.dish_id)
                .join(Ingredient, Ingredient.id == Recipe.ingredient_id)
                .filter(Dish.id == dish.get_id())
                .all()
            )
            for dish_id, unit, kcal, glucid, protein, canxi, lipid, category in result:
                if category == 'Vegetables':
                    vegetable_unit += unit
                    total_kcal += round(80*unit*kcal/100, 2)
                elif category == 'Fruits':
                    fruit_unit += unit
                    total_kcal += round(80*unit*kcal/100, 2)
                elif category == 'Grains':
                    grain_unit += unit
                    total_kcal += round((100*unit*20/glucid)*kcal/100, 2)
                elif category == 'Protein':
                    protein_unit += unit
                    total_kcal += round((100*unit*7/protein)*kcal/100, 2)
                elif category == 'Fats and oils':
                    fat_n_oil_unit += unit
                    total_kcal += round((100*unit*5/lipid)*kcal/100, 2)
                elif category == 'Dairy':
                    dairy_unit += unit
                    total_kcal += round((100*unit*100/canxi)*kcal/100, 2)
                elif category == 'Sugar':
                    sugar_unit += unit
                    total_kcal += round((5*unit)*kcal/100, 2)
                elif category == 'Salt and sauces':
                    salt_n_sauce_unit += unit
                    total_kcal += round((1*unit)*kcal/100, 2)

        vegetable_score = 10 * vegetable_unit / 3 if vegetable_unit < 3 else 10
        fruit_score = 10 * fruit_unit / 3 if fruit_unit < 3 else 10

        if grain_unit < 9:
            grain_score = 10 * grain_unit / 9
        elif grain_unit > 12:
            grain_score = 10 - (10 * (grain_unit - 12) / 12)
        else: grain_score = 10

        if protein_unit < 3:
            protein_score = 10 * protein_unit / 3
        elif protein_unit > 4:
            protein_score = 10 - (10 * (protein_unit - 4) / 4)
        else: protein_score = 10

        if dairy_unit < 1:
            dairy_score = 10 * dairy_unit / 1
        elif dairy_unit > 2:
            dairy_score = 10 - (10 * (dairy_unit - 2) / 2)
        else: dairy_score = 10

        if fat_n_oil_unit < 3:
            fat_n_oil_score = 10 * fat_n_oil_unit / 3
        elif fat_n_oil_unit > 4:
            fat_n_oil_score = 10 - (10 * (fat_n_oil_unit - 4) / 4)
        else: fat_n_oil_score = 10

        sugar_score = 10 - (10 * (sugar_unit - 5) / 5) if sugar_unit > 5 else 10
        salt_n_sauce_score = 10 - (10 * (salt_n_sauce_unit - 1) / 1) if salt_n_sauce_unit > 1 else 10
        total_VHEI_score = vegetable_score + fruit_score + grain_score + protein_score + dairy_score + fat_n_oil_score + sugar_score + salt_n_sauce_score

        user = User.query.get(self.uid)
        if not user:
            aim_score = 0
        else: 
            user_tdee = user.calculate_tdee()
            user_aim = user.get_aim()
            if user_aim == 'Giảm cân':
                aim_score = 100 * (user_tdee / total_kcal) if total_kcal > user_tdee else 100
            elif user_aim == 'Tăng cân':
                aim_score = 100 * (total_kcal / user_tdee) if total_kcal < user_tdee else 100
            else: aim_score = 100

        return  aim_score + total_VHEI_score

    def calculate_health_problem_score(self):
        num_dish_problem = 0
        user = User.query.get(self.uid)
        if not user:
            return 0
        else: 
            user_disease_id = user.get_disease_id()
            for dish in self.menu:
                result = (
                    db.session.query(Ingredient.name).join(Recipe, Recipe.ingredient_id == Ingredient.id)
                        .join(CannotEat, CannotEat.ingredient_id == Ingredient.id)
                        .join(Disease, Disease.id == CannotEat.disease_id)
                        .filter(Recipe.dish_id == dish.get_id(), Disease.id == user_disease_id).all() 
                )
                if len(result):
                    num_dish_problem += 1
            return (100 * (13 - num_dish_problem)) / 13
    
    def calculate_favorite_score(self):
        user = User.query.get(self.uid)
        if not user:
            return 0
        else: 
            user_favorite = (Favorite.query.filter_by(user_id=user.get_id()).all())
            favorite_dish_id = [favorite.dish_id for favorite in user_favorite]
            favorite_point = sum(5 for dish in self.menu if dish.get_id() in favorite_dish_id)
            return favorite_point


    def calculate_fitness_score(self):
        food_diversity_score = self.calculate_food_diversity_score()
        food_group_diversity_score = self.calculate_food_group_diversity_score()
        VHEI_calo_score = self.calculate_VHEI_calo_score()
        health_problem_score = self.calculate_health_problem_score()
        calculate_favorite_score = self.calculate_favorite_score()
        # print(calculate_favorite_score)
        return food_diversity_score+VHEI_calo_score+food_group_diversity_score+health_problem_score+calculate_favorite_score

  