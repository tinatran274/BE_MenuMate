import random
from models.dish import Dish, DishSchema

class MenuIndividual:
    MEAL_CATEGORIES = {'morning': 4, 'noon': 4, 'evening': 4, 'snack': 1}

    def __init__(self):
        self.menu = {category: self.generate_category(category) for category in self.MEAL_CATEGORIES}
        self.fitness = self.calculate_fitness()

    def generate_category(self, category):
        return [self.random_mutate() for _ in range(self.MEAL_CATEGORIES[category])]

    def calculate_fitness(self):
        return random.uniform(0, 1)

    def random_num(self, start, end):
        range_val = (end - start) + 1
        random_int = start + random.randint(0, range_val - 1)
        return random_int

    def random_mutate(self):
        dishs = Dish.query.all()
        length_data = len(dishs); 
        random_index = self.random_num(0, length_data-1); 
        return dishs[random_index]; 

    def to_dict(self):
        return {
            'menu': {category: [dish.to_dict() for dish in dishes] for category, dishes in self.menu.items()},
            'fitness': self.fitness
        }
    
    def calculate_total_lipid(self):
        total_lipid = 0
        for category, dishes in self.menu.items():
            for dish in dishes:
                dish_nutrition = dish.to_dict()
                total_lipid += dish_nutrition['total_lipid']
        return total_lipid
    
    def vegetables_score(self):

        consumed_servings = 1
        recommend_servings = 4
        return round(10*(consumed_servings/recommend_servings),2)

    def __getitem__(self, key):
        return self.menu[key]
