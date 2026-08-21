# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 16:49:34 2026

@author: madeleine.valat
"""

from link_matrix_into_drawio import identify_links_cluster,AssociationType,classes,associations

"""
 * @summary give ascii caracters to represent a UML relationship
 * @param {AssociationType} assoc_type - the type of the association
 * @ret {string} - a string to represent the relationship
"""
def represent_assoc(assoc_type):
    if assoc_type==AssociationType.METHOD:
        return "()"
    if assoc_type==AssociationType.HERITAGE:
        return "-|>"
    if assoc_type==AssociationType.ASSOCIATION:
        return "———"
    if assoc_type==AssociationType.NAVIGABLE_ASSOCIATION:
        return "X->"
    if assoc_type==AssociationType.DEPENDENCY:
        return "--->"
    if assoc_type==AssociationType.REALIZATION:
        return "-i->"
    if assoc_type==AssociationType.AGGREGATION:
        return "<>—"
    if assoc_type==AssociationType.COMPOSITION:
        return "◆——"
    return "—+—"

"""
 * @summary give a string to represent the direction of a UML relationship
 * @param {float} direction - a number representing the direction (negative or positive)
 * @ret {string} - a "+", "-" or " " depending of the direction given
"""
def represent_direction(direction):
    if direction<0:
        return "-"
    if direction>0:
        return "+"
    return " "

"""
 * @summary print the detailed relations in the models between two clusters, with the model where is the relation, a caracter representing if the relation is good directed or inversed, the term of the first cluster involved, a representation of the relationship and the term of the second cluster involved. The relation of type enumeration/attribute/method are print first.
 * @param {string} synonym1 - the centroid of the first cluster
 * @param {string} synonym2 - the centroid of the second cluster
 * @param {list(Association)} associations - the list of all the associations in the chosen models
 * @param {list(Element)} classes - the list of all the elements in the chosen models
"""
def detail_me_the_relations(synonym1,synonym2,associations,classes):
    links_between_clusters=identify_links_cluster(synonym1,synonym2,associations,classes)
    for link in links_between_clusters:
        if link["type"] in [AssociationType.ATTRIBUTE,AssociationType.ENUMERATION]:
            print(f"{link['client'].model}\t\t:{represent_direction(link['direction'])} {link['client'].name}\t{represent_assoc(link['type'])}\t{link['supplier'].name}")
    for link in links_between_clusters:
        if not link["type"] in [AssociationType.ATTRIBUTE,AssociationType.ENUMERATION]:
            print(f"{link['client'].model}\t\t:{represent_direction(link['direction'])} {link['client'].name}\t{represent_assoc(link['type'])}\t{link['supplier'].name}")
    return

# Just give the 2 cluster synonyms and then you can study the detail of the relations
c1=""
c2=""
while c1!="quit" and c2!="quit":
    c1=input("cluster 1 ?")
    c2=input("cluster 2 ?")
    detail_me_the_relations(c1,c2,associations,classes)