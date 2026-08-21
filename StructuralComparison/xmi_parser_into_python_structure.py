# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 14:51:10 2026

@author: madeleine.valat
"""

from enum import Enum
from bs4 import BeautifulSoup
from random import choice
import time
import sys
t0=time.time()

sys.path.append("")#TODO : write here the path of your project
# from model_terms_extraction_from_xmi import path,files,model_identifiers
from tools import identifier_models,path,files

from models_data_stockage import dict_id_clusters,dict_id_synonyms
identifier_selected_models=identifier_models(files)
clusters,synonyms=dict_id_clusters[identifier_selected_models],dict_id_synonyms[identifier_selected_models]
print(clusters,synonyms)
t1=time.time()
print(f"Preliminary calculations made in {t1-t0} s")

""" A structure to contain all the information about one cluster : id, common synonym of the terms in the cluster, terms that belong to the cluster and a color chosen randomly (for visualization)"""
class Cluster:
    def __init__(self,index,elements,synonym,color):
        self.index=index
        self.synonym=synonym
        self.elements=elements
        self.color=color
    
    def __str__(self):
        return self.synonym
    
    def __repr__(self):
        return str(self)+""

""" An enumeration class for the type of a UML object"""
class ElementType(Enum):
    CLASS = 0
    ABSTRACT_CLASS = 1
    INTERFACE = 2
    ENUMERATION = 3
    ENUMERATION_ELEMENT = 4
    METHOD = 5
    ATTRIBUTE = 6
    ASSOCIATION_CLASS=7

""" A structure to contain the interesting information of an element from a serious game model converted into UML (model name, semantic information held by the element, type in UML and cluster)"""
class Element:#can be a Class, a Method/Attribute of a Class, an Interface or an Enumeration class
    def __init__(self,name,model,elementType,cluster):
        self.id=model+"."+name
        self.name=name
        self.model=model
        self.type=elementType
        self.cluster=cluster.synonym
    
    def __str__(self):
        return f"{self.name} : {self.type} ({self.model}) - {self.cluster}"

    def __repr__(self):
        return str(self)

""" An enumeration class for the type of a UML relation"""
class AssociationType(Enum):
    ATTRIBUTE = 0
    METHOD = 1
    HERITAGE = 2
    ENUMERATION = 3
    ASSOCIATION = 4
    NAVIGABLE_ASSOCIATION = 5
    DEPENDENCY = 6
    REALIZATION = 7
    AGGREGATION = 8
    COMPOSITION = 9
    ASSOCIATION_CLASS = 10
 
""" A structure to contain the interesting information of an association from a serious game model converted into UML (model, name if existing, identifier of the ends, type of relation, multiplicity of the ends, if existing cluster of the name)"""       
class Association:
    def __init__(self,name,model,associationType,client,supplier,cluster=None,clientMultiplicity=None,supplierMultiplicity=None):
        self.id=model+"."+str(name)
        self.name=name
        self.model=model
        self.client=client
        self.supplier=supplier
        self.type=associationType
        self.multiplicity={"client":clientMultiplicity,"supplier":supplierMultiplicity}
        self.cluster=None
        if cluster is not None:
            self.cluster=cluster.synonym
    
    def __str__(self):
        return f"{self.client} {self.type} {self.supplier}"
    
    def __repr__(self):
        return str(self)

"""Initialization of the cluster colors, of the clusters list, and of the lists "classes" and "associations" """
random_color="#"+''.join([choice('0123456789ABCDEF') for j in range(6)])
clusters=[Cluster(i,clusters[i],synonyms[i],random_color) for i in range(len(clusters))]    

classes=[]
associations=[]

"""
 * @summary give the cluster corresponding to an element
 * @param {string} model - the name of the model in which the element appears
 * @param {string} term - the element name
 * @param {list(Cluster)} clusters - a list of Clusters containing the cluster informations for the classes of the xmi file "nom_fichier" 
 * @ret {Cluster} c - the Cluster in which the element is classified
"""
def cluster_of_element(model,term,clusters):
    term_to_search=model+"."+term
    for c in clusters:
        if term_to_search in c.elements:
            return c
    raise Exception(f"{term} not found in clusters !")

"""
 * @summary load the class, attributes and methods information in classes list, the implicit associations between the class and its attributes/method and heritages information in associations
 * @param {BeautifulSoup} xmi - the portion of structured xmi file related to the class
 * @param {list(Cluster)} clusters - a list of Clusters containing the cluster informations for the classes of the model
 * @param {string} model - the name of the model in which the element appears
 * @param {BeatifulSoup} full_xmi - the full structured xmi file
 * @param {boolean} interface - indicate if the class is an interface or not
"""
def add_class(xmi,clusters,model,full_xmi,interface=False):
    name=xmi.get("name")
    if name in ["Map(String,String)","StringToStringMapEntry"]:
        return
    elementType=ElementType.CLASS
    cluster=cluster_of_element(model, name, clusters)
    if interface:
        elementType=ElementType.INTERFACE
    if xmi.get("abstract"):
        elementType=ElementType.ABSTRACT_CLASS
    class_element=Element(name,model,elementType,cluster)
    classes.append(class_element)
    attributes=xmi.findAll("ownedAttribute")
    if attributes!=[]:
        for attr in attributes:
            attr_cluster=cluster_of_element(model,attr.get("name"),clusters)
            attr_element=Element(attr.get("name"),model,ElementType.ATTRIBUTE,attr_cluster)
            classes.append(attr_element)
            associations.append(Association(None, model, AssociationType.ATTRIBUTE, attr_element.id , class_element.id))
    methods=xmi.findAll("ownedOperation")
    if methods!=[]:
        for met in methods:
            met_cluster=cluster_of_element(model,met.get("name"),clusters)
            method_name=met.get("name")+"("
            for param in met.findAll("ownedParameter",direction="in"):
                method_name+=param.get("name")+" : "+param.get("type")+","
            if method_name[-1]==",":
                method_name=method_name[:-1]
            met_return=met.find("ownedParameter",direction="return")
            if met_return:
                method_name+=" : "+met_return.get("type")
            met_element=Element(method_name,model,ElementType.METHOD,met_cluster)
            classes.append(met_element)
            associations.append(Association(None, model, AssociationType.METHOD, met_element.id , class_element.id))
    for parent in xmi.findAll("generalization"):
        id_parent_xmi=parent.get("general")
        def class_parent(tag):
            return tag.get("xmi:id")==id_parent_xmi
        parent=full_xmi.find(class_parent)
        id_parent=model+"."+parent.get("name")
        associations.append(Association(None,model,AssociationType.HERITAGE,class_element.id,id_parent))
    return

"""
 * @summary using add_class, load the interface, attributes and methods information in classes list, the implicit associations between the interface and its attributes/method and heritages information in associations
 * @param {BeautifulSoup} xmi - the portion of structured xmi file related to the interface
 * @param {list(Cluster)} clusters - a list of Clusters containing the cluster informations for the classes of the model
 * @param {BeatifulSoup} full_xmi - the full structured xmi file
 * @param {string} model - the name of the model in which the element appears
"""
def add_interface(xmi,clusters,full_xmi,model):
    return add_class(xmi,clusters,model,full_xmi,interface=True)

"""
 * @summary load the enumeration name and elements in classes list and the corresponding implicit associations in associations list
 * @param {BeautifulSoup} xmi - the portion of structured xmi file related to the interface
 * @param {list(Cluster)} clusters - a list of Clusters containing the cluster informations for the classes of the model
 * @param {BeatifulSoup} full_xmi - the full structured xmi file
 * @param {string} model - the name of the model in which the element appears
"""
def add_enumeration(xmi,clusters,model):
    name=xmi.get("name")
    cluster_enum=cluster_of_element(model,name,clusters)
    element_enum=Element(name,model,ElementType.ENUMERATION,cluster_enum)
    classes.append(element_enum)
    possibilities=xmi.findAll("ownedLiteral")
    for poss in possibilities:
        name_poss=poss.get("name")
        cluster_poss=cluster_of_element(model,name_poss,clusters)
        element_poss=Element(name_poss,model,ElementType.ENUMERATION_ELEMENT,cluster_poss)
        classes.append(element_poss)
        associations.append(Association("", model, AssociationType.ENUMERATION, element_poss.id, element_enum.id))
    return

"""
 * @summary get the identifiers of the ends of a relationship
 * @param {BeautifulSoup} end1 - the portion of structured xmi file related to the 1st end
 * @param {BeautifulSoup} end2 - the portion of structured xmi file related to the 2nd end
 * @param {string} model - the name of the model in which the element appears
 * @param {BeatifulSoup} full_xmi - the full structured xmi file
 * @ret {string,string} the identifiers of the ends (model.name)
"""
def get_names_end(end1,end2,model,full_xmi):
    try:
        end1_type=end1.get("type")
        end2_type=end2.get("type")
    except:
        end1_type=end1
        end2_type=end2
    def end1_name(tag):
        return tag.get("xmi:id")==end1_type
    def end2_name(tag):
        return tag.get("xmi:id")==end2_type
    end1_id=model+"."+full_xmi.find(end1_name).get("name")
    end2_id=model+"."+full_xmi.find(end2_name).get("name")
    return end1_id,end2_id

"""
 * @summary get the multiplicity of an end of a relationship
 * @param {BeautifulSoup} wmi_end - the portion of structured xmi file related to the end
 * @ret {string} the end multiplicity (min..max)
"""
def multiplicity(xmi_end):
    mult=""
    lowerValue=xmi_end.get("lowerValue")
    upperValue=xmi_end.get("upperValue")
    if lowerValue or upperValue:
        mult="0.."
    if lowerValue:
        mult=str(lowerValue.get("value"))+".."
    if upperValue:
        mult+=str(upperValue.get("value"))
    else:
        mult+="n"
    return mult

"""
 * @summary load the association information in associations list
 * @param {string} model - the name of the model in which the element appears
 * @param {BeautifulSoup} xmi - the portion of structured xmi file related to the association
 * @param {BeatifulSoup} full_xmi - the full structured xmi file
"""
def add_association(model,xmi,full_xmi):
    end1,end2=xmi.findAll("ownedEnd")
    end1_id,end2_id=get_names_end(end1,end2,model,full_xmi)
    mult_end1=multiplicity(end1)
    mult_end2=multiplicity(end2)
    name=""
    if xmi.get("name"):
        name=xmi.get("name")
    
    # Navigability gestion
    if end1.get("isNavigable")=="True":
        id_client=end1_id
        mult_client=mult_end1
        id_supplier=end2_id
        mult_supplier=mult_end2
        associations.append(Association(name, model, AssociationType.NAVIGABLE_ASSOCIATION, id_client, id_supplier,clientMultiplicity=mult_client,supplierMultiplicity=mult_supplier))
        return
    elif end2.get("isNavigable")=="True":
        id_client=end2_id
        mult_client=mult_end2
        id_supplier=end1_id
        mult_supplier=mult_end2
        associations.append(Association(name, model, AssociationType.NAVIGABLE_ASSOCIATION, id_client, id_supplier,clientMultiplicity=mult_client,supplierMultiplicity=mult_supplier))
        return
    #Aggregations and compositions gestion
    if end1.get("aggregation")=="shared":
        id_client=end2_id
        mult_client=mult_end2
        id_supplier=end1_id
        mult_supplier=mult_end2
        associations.append(Association(name, model, AssociationType.AGGREGATION, id_client, id_supplier,clientMultiplicity=mult_client,supplierMultiplicity=mult_supplier))
        return
    elif end1.get("aggregation")=="composite":
        id_client=end2_id
        mult_client=mult_end2
        id_supplier=end1_id
        mult_supplier=mult_end2
        associations.append(Association(name, model, AssociationType.COMPOSITION, id_client, id_supplier,clientMultiplicity=mult_client,supplierMultiplicity=mult_supplier))
        return
    elif end2.get("aggregation")=="shared":
        id_client=end1_id
        mult_client=mult_end1
        id_supplier=end2_id
        mult_supplier=mult_end2
        associations.append(Association(name, model, AssociationType.AGGREGATION, id_client, id_supplier,clientMultiplicity=mult_client,supplierMultiplicity=mult_supplier))
        return
    elif end2.get("aggregation")=="composite":
        id_client=end1_id
        mult_client=mult_end1
        id_supplier=end2_id
        mult_supplier=mult_end2
        associations.append(Association(name, model, AssociationType.COMPOSITION, id_client, id_supplier,clientMultiplicity=mult_client,supplierMultiplicity=mult_supplier))
        return
    associations.append(Association(name, model, AssociationType.ASSOCIATION, end1_id, end2_id,clientMultiplicity=mult_end1,supplierMultiplicity=mult_end2))
    return

"""
 * @summary load the association information in associations list and the class in classes list
 * @param {BeautifulSoup} xmi - the portion of structured xmi file related to the interface
 * @param {list(Cluster)} clusters - a list of Clusters containing the cluster informations for the classes of the model
 * @param {string} model - the name of the model in which the element appears
 * @param {BeatifulSoup} full_xmi - the full structured xmi file
"""
def add_association_class(xmi,clusters,model,full_xmi):
    name=xmi.get("name")
    end1,end2=xmi.findAll("ownedEnd")
    id_end1,id_end2=get_names_end(end1, end2, model, full_xmi)
    cluster_class=cluster_of_element(model,name,clusters)
    classes.append(Element(name, model, ElementType.ASSOCIATION_CLASS, cluster_class))
    mult_end1=multiplicity(end1)
    mult_end2=multiplicity(end2)
    associations.append(Association(xmi.get("name"), model, AssociationType.ASSOCIATION_CLASS, id_end1, id_end2,clientMultiplicity=mult_end1,supplierMultiplicity=mult_end2,cluster=cluster_class))
    return

"""
 * @summary load the dependency information in associations list
 * @param {BeautifulSoup} xmi - the portion of structured xmi file related to the association
 * @param {BeatifulSoup} full_xmi - the full structured xmi file
 * @param {string} model - the name of the model in which the element appears
"""
def add_dependency(xmi,full_xmi,model):
    id_client,id_supplier=get_names_end(xmi.get("client"), xmi.get("supplier"), model, full_xmi)
    stereotype=None
    if xmi.find("appliedStereotype") is not None:
        stereotype=xmi.find("appliedStereotype").get("name")
    associations.append(Association(stereotype, model, AssociationType.DEPENDENCY, id_client, id_supplier))
    return 

"""
 * @summary load the realization information in associations list
 * @param {BeautifulSoup} xmi - the portion of structured xmi file related to the association
 * @param {BeatifulSoup} full_xmi - the full structured xmi file
 * @param {string} model - the name of the model in which the element appears
"""
def add_realization(xmi,full_xmi,model):
    id_client,id_supplier=get_names_end(xmi.get("client"), xmi.get("supplier"), model, full_xmi)
    associations.append(Association("",model,AssociationType.REALIZATION,id_client,id_supplier))
    return

"""
 * @summary load an xmi file from a path and add their classes and associations to two lists (classes & associations), taking into account the cluster of the semantic information held by the classes.
 * @param {string} chemin - The path to the repertory where are the xmi files
 * @param {string} nom_fichier - The name of the file in the repertory indicated by "chemin"
 * @param {list(Cluster)} clusters - A list of Clusters containing the cluster informations for the classes of the xmi file "nom_fichier" 
"""
def xmi_into_python_structures(chemin,nom_fichier,clusters):
    model=nom_fichier
    with open(chemin+nom_fichier+".xmi",'r',encoding='utf-8') as fichier_entree:
        content=fichier_entree.read()
        soup=BeautifulSoup(content,"xml")
        for element in soup.findAll("packagedElement"):
            if element.get("xmi:type")=="uml:Class":
                add_class(element,clusters,model,soup)
            elif element.get("xmi:type")=="uml:Interface":
                add_interface(element,clusters,soup,model)
            elif element.get("xmi:type")=="uml:Enumeration":
                add_enumeration(element,clusters,model)
            elif element.get("xmi:type")=="uml:Association":
                add_association(model,element,soup)
            elif element.get("xmi:type")=="uml:AssociationClass":
                add_association_class(element,clusters,model,soup)
            elif element.get("xmi:type")=="uml:Dependency":
                add_dependency(element,soup,model)
            elif element.get("xmi:type")=="uml:Realization":
                add_realization(element,soup,model)
            elif element.get("xmi:type") not in ["uml:DataType","uml:PrimitiveType"]:
                raise Exception("Type inconnu : "+element.get("xmi:type"))
    return 

"""Load all the xmi files in the "path" repertory in the classes and associations lists """
for file in files:
    # print(clusters)
    xmi_into_python_structures(path,file,clusters)#,['#676F35', '#6EF3D1', '#2619C1', '#1A70E7', '#C1B603', '#875A5A', '#3BC9F2', '#56A2E8', '#B6B7CB', '#ED9916', '#DF0BF9', '#7651DC', '#399814'])
# print(classes)
# for assoc in associations:
#     print(assoc)
        
t2=time.time()
print(f"Calculations ended in {t2-t1} s")
        
