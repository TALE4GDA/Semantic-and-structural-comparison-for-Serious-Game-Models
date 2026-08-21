# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 10:03:38 2026

@author: madeleine.valat
"""

import os

from models_data_stockage import model_identifiers

global_path=""# TODO : write here the path of your project
path=""# TODO : write here the path of the repertory containing the xmi files
files=[f.split(".")[0] for f in os.listdir(path)]

# files=files[0:6]+files[7:]
# files=files[0:1]+files[2:]

print(files)

"""
 * @summary generate the identifier from a model list
 * @param {list(string)} models_list - the list of model names
 * @ret {int} - a number corresponding to the sum of model identifiers
"""
def identifier_models(models_list):
    identifier=0
    for model in models_list:
        identifier+=model_identifiers[model]
    return identifier

"""
 * @summary get the model and the term from a string "model.term"
 * @param {string} term - a term like "model.term"
 * @ret {string,string} - the model name and the term
"""
def model_and_term_from(term):
    if "." not in term:
        return "",term
    i=0
    while len(term)>i and term[i]!=".":
        i+=1
    return term[:i+1],term[i+1:]

"""
 * @summary from a list of terms, extract a list of terms and a list of models corresponding to these terms
 * @param {list(string)} terms_list - a list of terms associated to the corresponding models (model.term)
 * @ret {list(string),list(string)} - two lists of the same length containing the models and the terms extracted from terms_list
"""
def extract_models_and_terms(terms_list):
    models=[]
    terms=[]
    for element in terms_list:
        model,term=model_and_term_from(element)
        models.append(model)
        terms.append(term)
    return models,terms

"""
 * @summary cluster the elements of a dendrogram depending on a given number of clusters
 * @param {array} cutree - An array indicating group membership at several agglomeration step (see scipy documentation of cut_tree return)
 * @param {list(string)} elements_names - the labels of the elements considered in the dendrogram
 * @param {int} nb_clusters - the desired number of clusters
 * @ret {list(list(string))} - a list of clusters (represented by lists of elements)
"""
def cut_hierarchy(cutree,elements_names,nb_clusters):
    if nb_clusters==1:
        return [elements_names]
    if nb_clusters==len(elements_names):
        return [[element] for element in elements_names]
    clusters=[[] for i in range(nb_clusters)]
    for index_cutree in range(len(cutree)):
        element_clustering=cutree[index_cutree][nb_clusters]
        element_name=elements_names[index_cutree]
        clusters[element_clustering].append(element_name)
    return clusters