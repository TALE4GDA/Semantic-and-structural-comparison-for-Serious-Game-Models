# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 10:44:49 2026

@author: madeleine.valat
"""

import time
from random import randint
import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import cut_tree
from vembed.vembed import calculate_similarities

from tools import extract_models_and_terms,identifier_models,files,cut_hierarchy,model_and_term_from
from models_data_stockage import dict_id_clusters,dict_id_synonyms,model_identifiers
from semantic_distance_model_terms import intermodel_similarity_calculation,make_dendrogram,models,symetrize

t0=time.time()

# Cluster calculation/determination
intermodel_distances=symetrize(1-intermodel_similarity_calculation(models))
hierarchy=make_dendrogram(intermodel_distances)

"""
 * @summary stock clusters' elements in a csv file
 * @param {list(list(string))} clusters - a list of clusters represented by lists of elements representing the terms associated to their models
 * @param {list(string)} synonyms - the synonyms corresponding to the clusters
 * @param {string} identifier - the number associated with the included models
"""
def visualize_clusters_in_table(clusters,synonyms,identifier):
    with open(f"Comparaison structurelle/Results/Clusters_informations/clusters{identifier}.csv","w") as f:
        for i in range(len(clusters)):
            c=extract_models_and_terms(clusters[i])[1]
            c.append(synonyms[i])
            similarities=calculate_similarities(c,c)[0]
            f.write(similarities.min().idxmax()+","+str(len(c)-1)+","+",".join(c[:-1])+"\n")

"""
 * @summary get the index of an element if this element is not already classified
 * @param {X} element - an element to test
 * @param {list(X)} liste - a list of elements
 * @param {list(int)} classification - the corresponding classifications of the elements in the list if existing
 * @ret {int} the index of the element in the list.
"""
def index(element,liste,classification):
    for i in range(len(liste)):
        if liste[i]==element and classification[i]==-1:
            return i
    raise Exception(f"{element} not found in list.")

"""
 * @summary calculate the silhouette score of a clustering passed in parameters (two ways to give the clustering : with clusters or with indexes_cluster)
 * @param {list(list(string))} df - a squared dataframe containing the matrix distance between the elements taken into account
 * @param {list(list(string))} clusters - a list of clusters represented by lists of elements representing the terms associated to their models
 * @param {list(int)} indexes_cluster - a proposition of clustering for the elements represented by df columns, formatted for scikit learn
 * @ret {float} - a score for the proposed clustering
"""
# Function generated thanks to chat gpt
def compute_silhouette_from_dataframe(df, clusters,indexes_cluster=None):
    """
    distance_matrix : array-like (n x n)
        Matrice de distances pré-calculée.
    clusters : list of lists
        Chaque sous-liste contient les indices des points appartenant au cluster.
        Exemple : [[0, 3, 5], [1, 2, 4]]
    """

    distance_matrix = np.array(df)
    np.fill_diagonal(distance_matrix, 0)
    n = distance_matrix.shape[0]

    # Vérification
    if distance_matrix.shape[0] != distance_matrix.shape[1]:
        raise ValueError("The distance matrix has to be a square.")
    
    for i in range(distance_matrix.shape[0]):
        for j in range(distance_matrix.shape[0]):
            mean=(distance_matrix[i][j]+distance_matrix[j][i])/2
            if mean<0:
                if mean>-0.00001:
                    mean=0
                else:
                    print(mean)
            distance_matrix[i][j]=mean
            distance_matrix[j][i]=mean
    
    if indexes_cluster is None:
        indexes_cluster=[-1 for i in range(distance_matrix.shape[0])]
        indexes_labels=df.columns
        # print(len(indexes_labels),distance_matrix.shape[0])
        for index_cluster in range(len(clusters)):
            for term in clusters[index_cluster]:
                index_term=index(term,indexes_labels,indexes_cluster)
                indexes_cluster[index_term]=index_cluster
        if -1 in indexes_cluster:
            ind=index(-1,indexes_cluster)
            print(ind,indexes_labels[ind])
            raise Exception("What is it ?")

    # Création du vecteur de labels
    # labels = np.empty(n, dtype=int)

    # for cluster_id, cluster in enumerate(indexes_cluster):
    #     for index in cluster:
    #         labels[index] = cluster_id

    # Calcul du silhouette score avec distances pré-calculées
    score=-1
    if len(set(indexes_cluster))>1 and len(set(indexes_cluster))<len(indexes_cluster):
        score = silhouette_score(distance_matrix, indexes_cluster, metric="precomputed")

    return score

# Generate cluster visualization file
identifier_selected_models=identifier_models(files)
clusters,synonyms=dict_id_clusters[identifier_selected_models],dict_id_synonyms[identifier_selected_models]
visualize_clusters_in_table(clusters, synonyms,identifier_selected_models)
t1=time.time()
print(f"Cluster visualization file generated in {t1-t0} s.")

# Calculate silhouette scores for different clusterings
df=(1-intermodel_similarity_calculation(models))/2
print("Our clustering silhouette score :",compute_silhouette_from_dataframe(df, clusters))
print("Maximal silhouette score of 100 random clustering :",max([compute_silhouette_from_dataframe(df, [],[randint(0,len(clusters)) for i in range(len(df))]) for j in range(0,100)]))
random_clusters_from_hierarchy=[]
dataset_len=len(intermodel_distances.columns)
cutree=cut_tree(hierarchy,range(0,dataset_len))
for i in range(100):
    clusters_proposition=cut_hierarchy(cutree,intermodel_distances.columns,randint(1,dataset_len))
    random_clusters_from_hierarchy.append(compute_silhouette_from_dataframe(df,clusters_proposition))
random_clusters_from_hierarchy.sort()
print("Silhouette scores for random clusters obtained cutting a dendrogram :",random_clusters_from_hierarchy)
t2=time.time()
print(f"Silhouette scores for clustering generated in {t2-t1} s.")

"""
 * @summary get the model corresponding to an identifier
 * @param {int} number - a power of 2 (isdentifier of one model)
 * @ret {string} - the model name
"""
def model_from_id(number):
    for model,identifier in model_identifiers.items():
        if identifier==number:
            return model
    raise Exception(f"Identifier {number} not found !")

"""
 * @summary get the models corresponding to an identifier
 * @param {int} identifier - a number (sum of the identifier of the concerned models)
 * @ret {list(string)} - the models name
"""
def models_from_id(identifier):
    bin_id=bin(identifier)[2:]
    models=[]
    for i in range(len(bin_id)):
        b=bin_id[i]
        if b=="1":
            models.append(model_from_id(2**(len(bin_id)-i-1)))
    return models
        
# count the number of termes per cluster and per model and stock the datas in a csv file
for identifier,clusters in dict_id_clusters.items():
    models=models_from_id(identifier)
    nb_clusters=len(clusters)
    df_clusters_models=pd.DataFrame([[0 for i in range(nb_clusters)] for j in range(len(models))])
    df_clusters_models.columns=dict_id_synonyms[identifier]
    df_clusters_models.index=models
    for index_cluster in range(nb_clusters):
        c=clusters[index_cluster]
        syn=df_clusters_models.columns[index_cluster]
        for term in c:
            m,t=model_and_term_from(term)
            m=m[:-1]
            df_clusters_models.loc[m,syn]+=1
    df_clusters_models.to_csv(f"Comparaison structurelle/Results/Clusters_informations/clusters_by_models{identifier}.csv", index=True)
        