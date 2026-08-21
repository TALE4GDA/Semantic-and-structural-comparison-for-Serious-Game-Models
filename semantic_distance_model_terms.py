# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 10:11:27 2025

@author: madeleine.valat
"""

from vembed.vembed import calculate_similarities
from scipy.cluster.hierarchy import linkage,dendrogram
import scipy.spatial.distance as ssd
import matplotlib.pyplot as plt

from model_terms_extraction_from_xmi import models

"""
 * @summary make two lists from models' vocabulary : one with only the terms, one with the terms associated with their models
 * @param {dict(string,list(string))} models_dict - A dictionary which contains for all models the list of terms in this model
 * @ret {list(string),list(string)} - a list with only the terms, a list with the terms associated to their models (model.term)
"""
def extract_terms_from(models_dict):
    terms_of_models=[]
    terms_of_models_with_models_name=[]
    for model_name,model_terms in models_dict.items():
        terms_of_models+=[term for term in model_terms]
        terms_of_models_with_models_name+=[str(model_name+"."+term) for term in model_terms]
    return terms_of_models,terms_of_models_with_models_name

"""
 * @summary generate a dataframe containing the similarities between the models' terms
 * @param {dict(string,list(string))} models_dict - A dictionary which contains for all models the list of terms in this model
 * @ret {DataFrame(float)} - A dataframe of semantic similarities between the models' terms
"""
def intermodel_similarity_calculation(models_dict):
    terms_of_models,terms_of_models_with_models_name=extract_terms_from(models_dict)
    similarities=calculate_similarities(terms_of_models, terms_of_models)[0]#choix de cos au lieu de dot pour des raisons d'intervalle et de similarité(a,a)=1
    similarities.columns=terms_of_models_with_models_name
    similarities.index=terms_of_models_with_models_name
    return similarities

"""
 * @summary make sure that a squared dataframe has 0 on its diagonal and is symetric
 * @param {DataFrame(float)} intermodel_similarities - A dataframe of semantic similarities between the models' terms
 * @ret {DataFrame(float)} - The same dataframe but with 0 on diagonal and symetrized
"""
def symetrize(intermodel_similarities):
    columns=intermodel_similarities.columns
    for i in columns:
        for j in columns:
            s_ij=intermodel_similarities.loc[i,j]
            s_ji=intermodel_similarities.loc[j,i]
            intermodel_similarities.loc[i,j]=max(0,s_ij)
            intermodel_similarities.loc[j,i]=max(0,s_ij)
            if i==j:
                intermodel_similarities.loc[i,j]=round(s_ij,0)
            elif s_ij!=s_ji:
                    mean=(s_ij+s_ji)/2
                    intermodel_similarities.loc[i,j]=mean
                    intermodel_similarities.loc[j,i]=mean
    return intermodel_similarities

"""
 * @summary make, save and print a dendrogram from a squared symetrized dataframe (cf documentation of linkage, from scipy)
 * @param {DataFrame(float)} distances - A dataframe of semantic similarities between the models' terms, symetric and with 0 on its diagonal
 * @ret {ndarray} - The hierarchical clustering encoded as a linkage matrix.
"""
def make_dendrogram(distances):
    hierarchy=linkage(ssd.squareform(distances),method='ward')
    plt.figure(figsize=(200, 80))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    dendrogram(
        hierarchy,
        color_threshold=0,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=8.,  # font size for the x axis labels
        labels=distances.columns
    )
    plt.savefig("dendrogram.png")
    plt.show()
    return hierarchy
