# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 17:35:53 2025

@author: madeleine.valat
"""

from vembed.vembed import calculate_similarities
from scipy.cluster.hierarchy import cut_tree
import pandas as pd
import time
from nltk.corpus import wordnet as wn
import matplotlib.pyplot as plt

from tools import identifier_models,model_and_term_from,extract_models_and_terms,cut_hierarchy
from semantic_distance_model_terms import intermodel_similarity_calculation,make_dendrogram,models,symetrize

intermodel_distances=symetrize(1-intermodel_similarity_calculation(models))
hierarchy=make_dendrogram(intermodel_distances)

t=time.time()

"""
 * @summary check if the two lists have exactly the same elements (taken into account the number of times an element appear)
 * @param {list(X)} list1 - a list of elements
 * @param {list(X)} list2 - a list of elements
 * @ret {boolean} - A boolean indicating if list1 and list2 contain the same elements
"""
def same_elements(list1,list2):
    return sorted(list1)==sorted(list2)

"""
 * @summary check if two clustering are equivalent (same number of clusters, same elements in each cluster)
 * @param {list(list(X))} clusters1 - a list of clusters (represented by lists of elements)
 * @param {list(list(X))} clusters2 - a list of clusters (represented by lists of elements)
 * @ret {boolean} - A boolean indicating if clusters1 and clusters2 are equivalents
"""
def same_elements_cluster(clusters1,clusters2):
    for c1 in clusters1:
        equivalent_c1=False
        for c2 in clusters2:
            if same_elements(c1,c2):
                clusters2.remove(c2)
                equivalent_c1=True
        if not equivalent_c1:
            return False
    return len(clusters2)==0

"""
 * @summary merged a set of lists
 * @param {list(list(X))} lists - a list of lists
 * @ret {list(X)} - a list containing all the elements of the lists passed in parameters
"""
def merge_lists(lists):
    merged_list=[]
    for liste in lists:
        merged_list+=liste
    return merged_list

"""
 * @summary calculate the apparition frequency of the elements in multiple lists
 * @param {list(list(string))} synonym_list - a list of lists of words (a list of words is supposed to represent all the synonyms of a term according to wordnet)
 * @ret {list(string,int,int)} - A list of triples : first a word from one of the lists passed in parameters, secund the number of lists containing this word and last the total number of lists
"""
def common_synonyms(synonym_list):
    nb_lists=len(synonym_list)
    synonyms=dict()
    for liste in synonym_list:
        if len(liste)==0:
            return None
        for syn in liste:
            if syn in synonyms.keys():
                synonyms[syn]+=1
            else:
                synonyms[syn]=1
    return [(syn,nb_syn,nb_lists) for syn,nb_syn in synonyms.items()]

assert common_synonyms([[],[]])==None
assert common_synonyms([["cat"],["cat"]])==[("cat",2,2)]
assert same_elements(common_synonyms([["cat","dog","rabbit"],["cat"]]),[("cat",2,2),("dog",1,2),("rabbit",1,2)])
assert same_elements(common_synonyms([["cat","dog","rabbit"],["dog"]]),[("dog",2,2),("cat",1,2),("rabbit",1,2)])
assert same_elements(common_synonyms([["cat","dog","rabbit","turtle"],["dog","cat","mouse"],["dog","mouse","cat"],["dog"]]),[("dog",4,4),("cat",3,4),("rabbit",1,4),("turtle",1,4),("mouse",2,4)])
common_synonyms([merge_lists(wn.synonyms("cat")),merge_lists(wn.synonyms("cat"))])

noms=["A","B","C","D"]
df=pd.DataFrame([[0,1,3,5],[1,0,2,4],[3,2,0,1],[5,4,1,0]])
df.columns=noms
df.index=noms
hierarchy_test=make_dendrogram(df)
cutree_test=cut_tree(hierarchy_test,range(0,5))  
assert same_elements_cluster(cut_hierarchy(cutree_test,noms,1),[noms])
assert same_elements_cluster(cut_hierarchy(cutree_test,noms,2),[["A","B"],["C","D"]])
assert same_elements_cluster(cut_hierarchy(cutree_test,noms,3),[["A","B"],["C"],["D"]])
assert same_elements_cluster(cut_hierarchy(cutree_test,noms,4),[["A"],["B"],["C"],["D"]])

"""
 * @summary calculate the most common synonyms for several lists of words.
 * @param {list(list(string))} cluster - a list of semantic clusters (represented by lists of words)
 * @param {float} threshold - a number between 0 and 1 indicating the minimal ratio of words which have to have a common synonym to elected a common synonym for a cluster
 * @ret {int/list(string,float)} - A list of doubles : first a word which is the common synonym of the cluster, second the ratio of this cluster's words which are synonym of this word. If no synonym is found, return 0 or None
"""
def find_cluster_synonym(cluster,threshold):
    word_synonymy=[[""] for i in range(len(cluster))]
    simple_words=[]
    mwe=[]#multi word expressions
    for term_index in range(len(cluster)):
        term=model_and_term_from(cluster[term_index])[1]
        try:
            word_synonymy[term_index]=merge_lists(wn.synonyms(term))
            if len(word_synonymy[term_index])>0:
                simple_words.append(term)
            else:
                mwe.append(term)
            word_synonymy[term_index].append(term)
        except:
            print("mwe")
            mwe.append(term)
            word_synonymy[term_index].append(term)
    if len(simple_words)==0:
        return 0
    weighted_synonyms=common_synonyms(word_synonymy)
    synonyms=[syn for syn,nb_syn,nb_lists in weighted_synonyms]
    if len(synonyms)==0:
        print("The problem is here")
        return None
    if len(mwe)>0:
        minimal_similarity_for_mwe=calculate_similarities(simple_words, synonyms)[0].min(axis=None)
        mwe_similarity=calculate_similarities(mwe, synonyms)[0]
        mwe_similarity.index=mwe
        mwe_similarity.columns=synonyms
    best_synonyms=[]
    best_synonymy_number=0
    nb_mwe=len(mwe)
    for syn,nb_syn,nb_lists in weighted_synonyms:
        nb_lists+=nb_mwe
        if nb_mwe>0:
            nb_syn+=mwe_similarity[mwe_similarity[syn]>=minimal_similarity_for_mwe].shape[0]
        synonymy_number=nb_syn/nb_lists
        if synonymy_number>=threshold:
            if synonymy_number>best_synonymy_number:
                best_synonymy_number=synonymy_number
                best_synonyms=[(syn,synonymy_number)]
            elif synonymy_number==best_synonymy_number:
                best_synonyms.append((syn,synonymy_number))
    if len(best_synonyms)<1:
        return None
    return best_synonyms

print(find_cluster_synonym(["cat","cat"],1))
assert ("cat",1) in find_cluster_synonym(["cat","cat"],1)
        
"""
 * @summary check if a clustering is valid regarding the common synonyms (the goal is here to select the higher threshold possible)
 * @param {list(list(string))} cluster_proposition - a list of cluster (represented by lists of words)
 * @param {float} threshold - a ratio indicating the minimal ratio of words which have to share a common synonym
 * @ret {boolean,boolean,list(string,float)} - A triple : a boolean indicating if the ratio is sufficiently low to elect a common synonym, a boolean indicating if it is possible to find a synonym (i.e. there is at least one word habving synonym(s) in a cluster), and a list of synonyms associated to a ratio
"""
def check_cluster_validity(cluster_proposition,threshold):
    synonyms=[]
    for c in cluster_proposition:
        cluster_validity=find_cluster_synonym(c,threshold)
        synonyms.append(cluster_validity)
        if cluster_validity is None:
            return False,True,[]
        if  cluster_validity==0:
            return True,False,[]
    return True,True,synonyms

"""
 * @summary calculate the clustering possible with given threshold for synonymy
 * @param {ndarray} hierarchy - a hierarchical clustering encoded as a linkage matrix
 * @param {list(string)} elements_names - the labels of the elements considered in the dendrogram
 * @param {float} threshold - a ratio indicating the minimal ratio of words which have to share a common synonym in a cluster
 * @param {int} nb_clusters - if known, the cluster number
 * @ret {list(list(string)),list(string)} - *A double containing a list of clusters (represented by lists of words) and a list of synonyms (each cluster is associated to a synonym)
"""
def perform_clustering(hierarchy,element_names,threshold,nb_clusters=1):
    print("Welcome in the clustering algorithm !")
    dataset_len=len(element_names)
    cutree=cut_tree(hierarchy,range(0,dataset_len))
    print("We have generated the desired trees")
    cluster_proposition=cut_hierarchy(cutree,element_names,nb_clusters)
    print("The first proposition is generated")
    cluster_validity=check_cluster_validity(cluster_proposition,threshold)
    print(cluster_validity)
    while nb_clusters<dataset_len and not cluster_validity[0]:
        nb_clusters+=1
        print("proposition n°"+str(nb_clusters)+" in progress...")
        cluster_proposition=cut_hierarchy(cutree, element_names, nb_clusters)
        cluster_validity=check_cluster_validity(cluster_proposition,threshold)
        if not cluster_validity[1]:
            nb_clusters=dataset_len
    if nb_clusters>=dataset_len:
        return [],[]
    return cluster_proposition,cluster_validity[2]

"""
 * @summary select the best threshold among the calculated ones
 * @param {list(float)} thresholds - a list of thresholds
 * @param {list(int)} cluster_numbers - a list of cluster numbers corresponding to the thresholds
 * @ret {float,int} - the higher threshold possible which produce more than 1 cluster and the corresponding number of clusters
"""
def higher_threshold_giving_clusters(thresholds,cluster_numbers):
    threshold_selected=thresholds[0]
    nb_clusters=cluster_numbers[0]
    for i in range(1,len(cluster_numbers)):
        if cluster_numbers[i]>=nb_clusters:
            threshold_selected=thresholds[i]
            nb_clusters=cluster_numbers[i]
    return threshold_selected,nb_clusters

"""
 * @summary calculate the best clustering (i.e. each cluster made has the higher possible ratio of words sharing a common synonym) and generate (and save) a figure to illustrate it.
 * @param {ndarray} hierarchy - a hierarchical clustering encoded as a linkage matrix
 * @param {list(string)} elements_names - the labels of the elements considered in the dendrogram
 * @param {int} identifier - the identifier of the model combination
 * @ret {float,int} - the higher threshold possible which produce more than 1 cluster and the corresponding number of clusters
"""
def select_higher_threshold(hierarchy,elements_names,identifier):
    fichier=open("synonymie.txt","a")
    fichier.write(str(identifier)+":\n")
    X=[]
    Y=[]
    for threshold in range(0,101,10):
        clusters,synonyms=perform_clustering(hierarchy,elements_names,threshold/100)
        fichier.write(str(clusters)+"\t"+str(threshold/100)+" : "+str(len(clusters))+"\n")
        # print(str(clusters)+"\t"+str(threshold/100)+" : "+str(len(clusters))+"\n")
        X.append(threshold)
        Y.append(len(clusters))
        if len(clusters)==0:
           X+=[s for s in range(threshold+10,101,10)]
           Y+=[0 for s in range(threshold+10,101,10)]
           break
    new_start,nb_clusters=higher_threshold_giving_clusters(X,Y)
    for threshold in range(new_start,new_start+10,1):
        clusters,synonyms=perform_clustering(hierarchy,elements_names,threshold/100)
        fichier.write(str(clusters)+"\t"+str(threshold/100)+" : "+str(len(clusters))+"\n")
        # print(str(clusters)+"\t"+str(threshold/100)+" : "+str(len(clusters))+"\n")
        X.append(threshold)
        Y.append(len(clusters))
        if len(clusters)==0:
           X+=[s for s in range(threshold+1,new_start+10,1)]
           Y+=[0 for s in range(threshold+1,new_start+10,1)]
           break
    X=X[:new_start//10+1]+X[12:]+X[new_start//10+1:11]
    Y=Y[:new_start//10+1]+Y[12:]+Y[new_start//10+1:11]
    plt.plot(X,Y)
    plt.savefig(f"nb_clusters_by_threshold{identifier}.png")
    plt.show()
    return higher_threshold_giving_clusters(X,Y)

"""
 * @summary select one synonym per cluster
 * @param {list(list(string)),list(list(string,float))} clusters_and_synonyms - A double containing a list of clusters (represented by lists of words) and a list of synonyms (represented by lists of doubles : first a word which is the common synonym of the cluster, second the ratio of this cluster's words which are synonym of this word)
 * @ret {list(list(string)),list(string,float)} - the cluster list and the corresponding synonym list
"""
def cluster_centroids(clusters_and_synonyms):
    clusters,common_synonyms=clusters_and_synonyms
    clusters_centroids=["" for c in clusters]
    for index_cluster in range(len(clusters)):
        cluster_with_common_synonym=extract_models_and_terms(clusters[index_cluster])[1]+[common_synonyms[index_cluster][0][0]]
        intern_similarities=calculate_similarities(cluster_with_common_synonym,cluster_with_common_synonym)[0]
        clusters_centroids[index_cluster]=intern_similarities.min().idxmax()
    return clusters,clusters_centroids

"""
 * @summary write python instructions to represent the clustering and the corresponding synonyms when needed
 * @param {list(string)} models - the list of models used to extract terms and then perform the clustering
 * @param {list(list(string)) clusters - a list of clusters (represented by lists of words)
 * @param {list(string,float)} - the corresponding synonym list (associated with ratios)
"""
def write_clusters_in_python_file(models,clusters,synonyms):
    with open("models_data_stockage.py","a") as output_file:
        identifier=identifier_models(models)
        to_write=f"\n\ndict_id_models[{identifier}]={list(models)}\ndict_id_clusters[{identifier}]={clusters}\ndict_id_synonyms[{identifier}]={synonyms}"
        output_file.write(to_write)
    return

threshold,nb_clusters=select_higher_threshold(hierarchy, intermodel_distances.columns,identifier_models(models.keys()))
threshold=threshold/100
print(threshold,nb_clusters)
clusters,synonyms=cluster_centroids(perform_clustering(hierarchy,intermodel_distances.columns,threshold,nb_clusters=nb_clusters))
print(clusters,synonyms)
write_clusters_in_python_file(models.keys(), clusters, synonyms)

print(time.time()-t)



