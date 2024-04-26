import random
from models.dish import Dish, DishSchema
from models.recipe import Recipe, RecipeSchema
from models.ingredient import Ingredient
from genetic_algorithm.menu_individual import MenuIndividual
from extension import db, ma 
import numpy as np
import pandas as pd

class GeneticAlgorithm:
    MEAL_CATEGORIES = {'morning': 4, 'noon': 4, 'evening': 4, 'snack': 1}
    
    def __init__(self, population_size, mutation_rate, generation, uid):
        self.uid = uid
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generation = generation
        self.population = self.initialize_population()

    def initialize_population(self):
        return [MenuIndividual(self.uid) for _ in range(self.population_size)]
    

    def random_selection(self, fitness_scores):
        sorted_indices = np.argsort(fitness_scores)[::-1].tolist()
        selected_population = [self.population[i] for i in sorted_indices[:self.population_size // 2]]
        return selected_population
    

    def one_point_crossover(self, parent1, parent2):
        menu_parent1 = parent1.menu
        menu_parent2 = parent2.menu
        len_individual = len(menu_parent1)
        crossover_point = random.randint(1, len_individual - 1) if random.random() < self.mutation_rate else 0
        menu_child1 = menu_parent1[:crossover_point] + menu_parent2[crossover_point:]
        menu_child2 = menu_parent2[:crossover_point] + menu_parent1[crossover_point:]
        child1 = MenuIndividual(self.uid, menu_child1)
        child2 = MenuIndividual(self.uid, menu_child2)
        return child1, child2 

    def random_num(self, start, end):
        range_val = (end - start) + 1
        random_int = start + random.randint(0, range_val - 1)
        return random_int

    def random_dish(self):
        dishs = Dish.query.all()
        length_data = len(dishs); 
        random_index = self.random_num(0, length_data - 1); 
        return dishs[random_index]; 

    def random_mutate(self, menu):
        list_menu = menu.menu
        len_individual = len(list_menu)    
        mutate_point = random.randint(1, len_individual - 1) if random.random() < self.mutation_rate else 0
        list_menu[mutate_point] = self.random_dish()
        result = MenuIndividual(self.uid, list_menu)
        return result

    def main_genetic_algorithm(self):
        best_menu = self.population[0]
        for _ in range(self.generation):
            fitness_scores = [menu.get_fitness() for menu in self.population]
            print(fitness_scores)
            selected_parents = self.random_selection(fitness_scores)
            children = []
            for _ in range(self.population_size // 2 ):
                parent1, parent2 = random.sample(selected_parents, 2)
                child1, child2 = self.one_point_crossover(parent1, parent2)
                child1 = self.random_mutate(child1)
                child2 = self.random_mutate(child2)
                children.extend([child1, child2])
            self.population = children

        best_menu = max(self.population, key=lambda menu: menu.get_fitness())
        return best_menu.to_dict()
