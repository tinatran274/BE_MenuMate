import random
from models.favorite import Favorite
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from extension import db, ma 
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
        self.user_item_matrix = self.get_user_item_matrix()
        self.k = k

    def get_user_item_matrix(self):
        favorites = Favorite.query.all()
        users = set(f.user_id for f in favorites)
        dishes = set(f.dish_id for f in favorites)
        self.n_user_id = list(users)
        self.m_dish_id = list(dishes)
        user_item_matrix = [[0] * len(dishes) for _ in range(len(users))]
        user_index_map = {user: i for i, user in enumerate(users)}
        dish_index_map = {dish: i for i, dish in enumerate(dishes)}
        for favorite in favorites:
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
        pca = PCA(n_components=2)
        pca.fit(user_item_matrix)
        transformed_matrix = pca.transform(user_item_matrix)
        self.dim_reduced_matrix = transformed_matrix
        return user_item_matrix
    
    def find_k(self):
        range_k = [2, 3]
        silhouette_avg = []
        for i in range_k:
            kmeans = KMeans(n_clusters=i, random_state=42, n_init=10)
            kmeans.fit(self.dim_reduced_matrix)
            predicted_clusters = kmeans.predict(self.dim_reduced_matrix)
            silhouette_avg.append(silhouette_score(self.dim_reduced_matrix, predicted_clusters))        
        max_score = np.argmax(silhouette_avg)
        return range_k[max_score]

    def run_kmeans(self):
        n = self.find_k()
        kmeans = KMeans(n_clusters=n, random_state=40, n_init=10)
        kmeans.fit(self.dim_reduced_matrix)
        self.label_cluster = kmeans.labels_
        for index, value in enumerate(self.n_user_id):
            if value == self.uid:
                indices = index
                break
        return indices


    def generate_recommendations(self):
        recommendations = []
        user_cluster_indices = self.run_kmeans()
        user_cluster = self.label_cluster[user_cluster_indices]
        other_users_indices = [i for i, x in enumerate(self.label_cluster) 
                       if x == user_cluster]
        other_users_indices.remove(user_cluster_indices)
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

        # print(list_weight) 

        return list_weight




