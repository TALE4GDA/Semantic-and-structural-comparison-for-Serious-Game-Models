# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 11:31:06 2026

@author: madeleine.valat
"""

from bs4 import BeautifulSoup

from tools import global_path,path,files

"""
 * @summary make a list of terms from a portion of an xmi file which describe a class
 * @param {BeautifulSoup} xmi - a structured portion of an xmi file describing the class
 * @param {boolean} interface - indicate if the class is an interface
 * @ret {list(string)} - the list of terms extracted from the xmi portion
"""
def extract_terms_from_class(xmi,interface=False):
    terms=[]
    name=xmi.get("name")
    if name in ["Map(String,String)","StringToStringMapEntry"]:
        return terms
    terms.append(name)
    attributes=xmi.findAll("ownedAttribute")
    if attributes!=[]:
        for attr in attributes:
            terms.append(attr.get("name"))
    methods=xmi.findAll("ownedOperation")
    if methods!=[]:
        for met in methods:
            terms.append(met.get("name"))
    return terms

"""
 * @summary make a list of terms from a portion of an xmi file which describe an interface, using extract_terms_from_class
 * @param {BeautifulSoup} xmi - a structured portion of an xmi file describing the interface
 * @ret {list(string)} - the list of terms extracted from the xmi portion
"""
def extract_terms_from_interface(xmi):
    return extract_terms_from_class(xmi,interface=True)

"""
 * @summary make a list of terms from a portion of an xmi file which describe an enumeration
 * @param {BeautifulSoup} xmi - a structured portion of an xmi file describing the enumeration
 * @ret {list(string)} - the list of terms extracted from the xmi portion
"""
def extract_terms_from_enumeration(xmi):
    terms=[]
    terms.append(xmi.get("name"))
    possibilities=xmi.findAll("ownedLiteral")
    for poss in possibilities:
        terms.append(poss.get("name"))
    return terms

"""
 * @summary make a list of terms from a portion of an xmi file which describe an association class, using extract_terms_from_class
 * @param {BeautifulSoup} xmi - a structured portion of an xmi file describing the association class
 * @ret {list(string)} - the list of terms extracted from the xmi portion
"""
def extract_terms_from_association_class(xmi):
    return extract_terms_from_class(xmi)

"""
 * @summary extract all the terms from the UML class diagram described by several xmi files
 * @param {string} path - the path of the repertory containing the xmi files
 * @param {list(string)} models_names - The models' names
 * @ret {dict(string,list(string))} - a dictionary mapping the models' names to their corresponding terms' list (each term appear once)
"""
def extract_terms_from_xmi(path,models_names):
    dict_model_terms=dict()
    for model in models_names:
        dict_model_terms[model]=[]
        with open(path+model+".xmi",'r',encoding='utf-8') as input_file:
            content=input_file.read()
            soup=BeautifulSoup(content,"xml")
            for element in soup.findAll("packagedElement"):
                if element.get("xmi:type")=="uml:Class":
                    dict_model_terms[model]+=extract_terms_from_class(element)
                elif element.get("xmi:type")=="uml:Interface":
                    dict_model_terms[model]+=extract_terms_from_interface(element)
                elif element.get("xmi:type")=="uml:Enumeration":
                    dict_model_terms[model]+=extract_terms_from_enumeration(element)
                elif element.get("xmi:type")=="uml:AssociationClass":
                    dict_model_terms[model]+=extract_terms_from_association_class(element)
    for model,terms in dict_model_terms.items():
        dict_model_terms[model]=list(set(terms))
    return dict_model_terms

"""
 * @summary generate an id for each model. These id have to be summable to generate a unique id for each model combination (so each model is associated to a power of 2)
 * @param {list(string)} full_model_list - the full list of the models considered
 * @ret {dict(string,int)} - a dictionary mapping each model to the selected id for this model
"""
def generate_identifier_models(full_model_list):
    identifiers_model=dict()
    for index in range(len(full_model_list)):
        model=full_model_list[index]
        identifiers_model[model]=2**index
    return identifiers_model

models=extract_terms_from_xmi(path,files)
print(models)
model_identifiers=generate_identifier_models(files)

try:
    from models_data_stockage import model_identifiers
except:
    with open(global_path+"/models_data_stockage.py","a") as output_file:
        output_file.write("\n")
        output_file.write(f"model_identifiers={model_identifiers}")
    
