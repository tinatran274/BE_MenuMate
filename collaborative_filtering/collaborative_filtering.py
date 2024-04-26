import random
from models.favorite import Favorite
from models.user import User
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

class CollaborativeFiltering:
    def __init__(self, uid, k):
        self.uid = uid
        self.m_dish_id = []
        self.n_user_id = []
        self.label_cluster = []
        self.dim_reduced_matrix = []
        self.user_average = []
        self.user_data_matrix = self.get_user_data_matrix()
        self.user_item_matrix = self.get_user_item_matrix()
        self.k = k

    def convert_gender(self, value):
        if value == 'Nữ':
            return 0
        else:
            return 1
        
    def convert_exercise(self, value):
        if value == 'Vận động nhẹ (1-3 ngày/tuần)':
            return 1.375
        elif value == 'Vận động vừa phải (4-5 ngày/tuần)':
            return 1.55
        elif value == 'Vận động nhiều (6-7 ngày/tuần)':
            return 1.9
        return 1.2
    
    def convert_aim(self, value):
        if value == 'Giảm cân':
            return 3
        elif value == 'Giữ cân':
            return 2
        return 1
        
    def normalize_user_data(self, user_data):
        num_cols = len(user_data[0])
        for row in user_data:
            row[3] = self.convert_gender(row[3])
            row[4] = self.convert_exercise(row[4])
            row[5] = self.convert_aim(row[5])
        mins = [min(row[i] for row in user_data) for i in range(num_cols)]
        maxs = [max(row[i] for row in user_data) for i in range(num_cols)]
        for row in user_data:
            for i in range(num_cols):
                min_val = mins[i]
                max_val = maxs[i]
                row[i] = (row[i] - min_val) / (max_val - min_val)
        return user_data

    def get_user_data_matrix(self):
        users = User.query.all()
        user_list = [[u.age, u.height, u.weight, u. gender, u.exercise, u.aim] for u in users]
        user_data_matrix = self.normalize_user_data(user_list)
        pca = PCA(n_components=2)
        pca.fit(user_data_matrix)
        transformed_matrix = pca.transform(user_data_matrix)
        self.dim_reduced_matrix = transformed_matrix
        return user_data_matrix

    def get_user_item_matrix(self):
        favorites_list = Favorite.query.all()
        users_list = User.query.all()
        users = set(u.id for u in users_list)
        dishes = set(f.dish_id for f in favorites_list)
        self.n_user_id = list(users)
        self.m_dish_id = list(dishes)
        user_item_matrix = [[0] * len(self.m_dish_id) for _ in range(len(self.n_user_id))]
        user_index_map = {user: i for i, user in enumerate(self.n_user_id)}
        dish_index_map = {dish: i for i, dish in enumerate(self.m_dish_id)}
        for favorite in favorites_list:
            user_index = user_index_map[favorite.user_id]
            dish_index = dish_index_map[favorite.dish_id]
            user_item_matrix[user_index][dish_index] = 1
        row_averages = []
        for row in user_item_matrix:
            total = 0
            num_items = 0
            for item in row:
                total += item
                num_items += 1
            ave = total/num_items
            row_averages.append(ave)
        self.user_average=row_averages
        return user_item_matrix
    
    def find_k(self):
        print(self.user_data_matrix)
        print(self.user_item_matrix)
        range_k = [2, 3, 4, 5]
        silhouette_avg = []
        for i in range_k:
            kmeans = KMeans(n_clusters=i, random_state=42, n_init=10)
            kmeans.fit(self.dim_reduced_matrix)
            predicted_clusters = kmeans.predict(self.dim_reduced_matrix)
            silhouette_avg.append(silhouette_score(self.dim_reduced_matrix, predicted_clusters))        
        max_score = np.argmax(silhouette_avg)
        print('k', range_k[max_score])
        return range_k[max_score]

    def run_kmeans(self):
        n = self.find_k()
        kmeans = KMeans(n_clusters=n, random_state=40, n_init=10)
        kmeans.fit(self.dim_reduced_matrix)
        self.label_cluster = kmeans.labels_
        print('label_cluster', self.label_cluster)
        for index, value in enumerate(self.n_user_id):
            if value == self.uid:
                indices = index
                break
        return indices


    def generate_recommendations(self):
        user_cluster_indices = self.run_kmeans()
        user_cluster = self.label_cluster[user_cluster_indices]
        other_users_indices = [i for i, x in enumerate(self.label_cluster) 
                       if x == user_cluster]
        other_users_indices.remove(user_cluster_indices)
        if len(other_users_indices):
            other_user = [self.user_item_matrix[i] for i in other_users_indices]

            cosine_similarities = cosine_similarity([self.user_item_matrix[user_cluster_indices]],
                                                    other_user) 
            sorted_neighbor_indices = [value for _, value in sorted(zip(cosine_similarities[0], 
                                                                        other_users_indices), reverse=True)]
            sorted_cosine_similarities = sorted(cosine_similarities[0], reverse=True)
            sorted_average = [self.user_average[i] for i in sorted_neighbor_indices]
            k_nearest_neighbors = sorted_neighbor_indices[:self.k]
            list_weight = []
            user_rating = self.user_item_matrix[user_cluster_indices]
            item_indices = [index for index, value in enumerate(user_rating) if value == 0]
            for item in item_indices:
                numerator = 0
                denominator = 0
                for index, neighbor in enumerate(k_nearest_neighbors):
                    print(item, index, neighbor, self.user_item_matrix[neighbor][item])
                    if self.user_item_matrix[neighbor][item] != 0:
                        numerator += sorted_cosine_similarities[index] * (self.user_item_matrix[neighbor][item]-sorted_average[index])
                        denominator += sorted_cosine_similarities[index]
                if denominator == 0:
                    weight = 0
                else:
                    weight = numerator / denominator
                weight += self.user_average[user_cluster_indices]
                list_weight.append(weight)
            sorted_data = sorted(list(zip(item_indices, list_weight)), key=lambda x: x[1], reverse=True) 
            sorted_indices_recommend = [item[0] for item in sorted_data]
            print(item_indices)
            print(list_weight)
            print(sorted_indices_recommend)
            recommended_dishes = [self.m_dish_id[i] for i in sorted_indices_recommend]
            return recommended_dishes
        else: 
            trans_user_item_matrix = [[row[i] for row in self.user_item_matrix] for i in range(len(self.user_item_matrix[0]))]
            row_sum = []
            for row in trans_user_item_matrix:
                total = 0
                for item in row:
                    total += item
                row_sum.append(total)
            sorted_dish_indices = [value for _, value in sorted(zip(row_sum, self.m_dish_id), reverse=True)]
            print(sorted_dish_indices)
            recommended_dishes = [self.m_dish_id[i] for i in sorted_dish_indices]
            print(recommended_dishes)
            return recommended_dishes




