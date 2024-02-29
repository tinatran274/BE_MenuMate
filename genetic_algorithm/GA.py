
import numpy as np
import pandas as pd
import random


df = pd.read_csv('nutrients_csvfile.csv', encoding='ISO-8859-1')
df.iloc[:, 2:9] = df.iloc[:, 2:9].apply(pd.to_numeric, errors='coerce').fillna(0)
data_list = []
for row in df:
    data_list = df.values.tolist()


num_group_morning = 3
num_group_lunch = 4
num_group_dinner = 4
num_group_snack = 1
total_group = 12 #num_genes

G1 = ['Dairy products']
G2 = ['Breads, cereals, fastfood,grains']
G3 = ['Fish, Seafood','Meat, Poultry']
G4 = ['Fats, Oils, Shortenings']
G5 = ['Vegetables A-E', 'Vegetables R-Z', 'Vegetables F-P']
G6 = ['Fruits A-F', 'Fruits G-P', 'Fruits R-Z']
G7 = ['Seeds and Nuts']
G8 = ['Soups']
G9 = ['Desserts, sweets', 'Drinks,Alcohol, Beverages', 'Jams, Jellies']

population_size = 25
num_generations = 50
mutation_rate = 0.2

def random_num(start, end):
    range_val = (end - start) + 1
    random_int = start + random.randint(0, range_val - 1)
    return random_int

def calculate_fitness_morning(morning_menu):
    point = 0
    point -= len(morning_menu)-len(set(item[9] for item in morning_menu))
    for item in morning_menu:
        point += 1 if (item[9] in G1) else 0
        point += 1 if (item[9] in G2) else 0
        point += 1 if (item[9] in G6) else 0
        point += 1 if (item[9] in G5) else 0
        point += 1 if (item[9] in G8) else 0

    return point

def calculate_fitness_lunch(lunch_menu):
    point = 0
    point -= len(lunch_menu)-len(set(item[9] for item in lunch_menu))
    for item in lunch_menu:     
        point += 1 if (item[9] in G2) else 0
        point += 1 if (item[9] in G3) else 0
        point += 1 if (item[9] in G5) else 0
        point += 1 if (item[9] in G6) else 0
        point += 1 if (item[9] in G8) else 0

    return point

def calculate_fitness_dinner(dinner_menu):
    point = 0
    point -= len(dinner_menu)-len(set(item[9] for item in dinner_menu))
    for item in dinner_menu:
        point += 1 if (item[9] in G2) else 0
        point += 1 if (item[9] in G3) else 0
        point += 1 if (item[9] in G5) else 0
        point += 1 if (item[9] in G6) else 0
            
    return point

def calculate_fitness_snack(snack_menu):
    point = 0
    point -= len(snack_menu)-len(set(item[9] for item in snack_menu))
    for item in snack_menu:
        point += 1 if (item[9] in G1) else 0
        point += 1 if (item[9] in G6) else 0
        point += 1 if (item[9] in G7) else 0
        point += 1 if (item[9] in G9) else 0
            
    return point


def calculate_fitness(menu):
    point = 0 
    morning_group = []
    lunch_group = []
    dinner_group = []
    snack_group = []

    for index, item in enumerate(menu):
        if index < num_group_morning:
            morning_group.append(item)
        elif index < num_group_morning + num_group_lunch:
            lunch_group.append(item)
        elif index < num_group_morning + num_group_lunch + num_group_dinner:
            dinner_group.append(item)
        else:
            snack_group.append(item)
    
    point += calculate_fitness_morning(morning_group)
    point += calculate_fitness_lunch(lunch_group)
    point += calculate_fitness_dinner(dinner_group)
    point += calculate_fitness_snack(snack_group)
    # point += calculate_fitness_nutrient(menu)
    
    return point

def mutated_genes():
    length_data = len(data_list); 
    random_index = random_num(0, length_data-1); 
    return data_list[random_index]; 

def create_menu():
    menu_list = []
    for i in range(total_group):
        menu_list.append(mutated_genes())
    return menu_list

def create_init_population():
    return [create_menu() for _ in range(population_size)]

def random_selection(population, fitness_scores):
    sorted_indices = np.argsort(fitness_scores)[::-1].tolist()
    selected_population = [population[i] for i in sorted_indices[:population_size // 2]]
    
    return selected_population

def one_point_crossover(parent1, parent2):
    crossover_point = random.randint(1, total_group - 1) if random.random() < mutation_rate else 0
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    
    return child1, child2

def random_mutate(menu):
    for i in range(total_group):
        if random.uniform(0, 1) < mutation_rate:
            menu[i] = random.choice(data_list)
    return menu

def print_menu(menu):
    total_calo = 0
    morning_group = []
    lunch_group = []
    dinner_group = []
    snack_group = []

    for index, item in enumerate(menu):
        if index < num_group_morning:
            morning_group.append(item)
        elif index < num_group_morning + num_group_lunch:
            lunch_group.append(item)
        elif index < num_group_morning + num_group_lunch + num_group_dinner:
            dinner_group.append(item)
        else:
            snack_group.append(item)
            
    print('Bữa sáng: ', morning_group)
    print('Bữa trưa: ', lunch_group)
    print('Bữa tối: ', dinner_group)
    print('Bữa nhẹ: ', snack_group)
    print('point: ', calculate_fitness(menu))
    
    for row in menu:
        total_calo += int(row[3])
    print('Total calories: ', total_calo)

def genetic_algorithm():
    population = create_init_population()
    best_menu = population[0]
    # best_solution = calculate_fitness(best_menu)
    # count_loop = 0
    for _ in range(num_generations):
    # while (best_solution < 16):
        fitness_scores = [calculate_fitness(menu) for menu in population]
        selected_parents = random_selection(population, fitness_scores)
        children = []
        for _ in range(population_size):
            parent1, parent2 = random.sample(selected_parents, 2)
            child1, child2 = one_point_crossover(parent1, parent2)
            child1 = random_mutate(child1)
            child2 = random_mutate(child2)
            children.extend([child1, child2])
        population = children
    best_menu = max(population, key=calculate_fitness)
        # best_solution = calculate_fitness(best_menu)
        # count_loop += 1
    # best_solution = max(population, key=calculate_fitness)
    # print('Count loop:',count_loop)
    return best_menu

# optimized_menu = genetic_algorithm()
# print("Optimized Menu:", optimized_menu)
# print_menu(optimized_menu)


