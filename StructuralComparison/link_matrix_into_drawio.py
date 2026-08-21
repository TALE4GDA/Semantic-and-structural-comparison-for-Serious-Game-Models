# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 10:54:21 2026

@author: madeleine.valat
"""

import pandas as pd
from random import randint
import time
t0=time.time()

from xmi_parser_into_python_structure import AssociationType,classes,associations,identifier_selected_models

attr="atributes"
meth="methods"
enum="enumerate"

"""
 * @summary find an element in a list based on an identifier
 * @param {string} id_element - the id of the element ("model.term")
 * @param {list(Element)} list_elements - a list of elements (supposed to be "classes" list)
 * @ret {Element} - the element associated with the id.
"""
def find_by_id(id_element,list_elements):
    for element in list_elements:
        if element.id==id_element:
            return element
    raise Exception(f"The element of id '{id_element}' was not found in the list.")

"""
 * @summary get the index of an element in a list
 * @param {X} element - the element to search
 * @param {list(X)} list_of_elements - a list of elements
 * @ret {int} - the index of the element.
"""
def index(element,list_of_elements):
    for i in range(len(list_of_elements)):
        if list_of_elements[i]==element:
            return i
    raise Exception(f"{element} not found in the list !")

"""
 * @summary calculate the number of terms per model and per cluster
 * @param {list(Element)} classes - the list of elements from models (classes)
 * @ret {DataFrame(int)} - a dataframe with in rows the models, in columns the cluster centroids, which represent the number of terms per cluster and per model.
"""
def identify_models_in_clusters(classes):
    centroids=[]
    models=[]
    for element in classes:
        if element.cluster not in centroids:
            centroids.append(element.cluster)
        if element.model not in models:
            models.append(element.model)
    columns=centroids
    rows=models
    models_in_cluster=[[0 for c in columns] for r in rows]
    for element in classes:
        index_row=index(element.model,rows)
        index_column=index(element.cluster,columns)
        models_in_cluster[index_row][index_column]+=1
    df_models_in_clusters=pd.DataFrame(models_in_cluster)
    df_models_in_clusters.columns=columns
    df_models_in_clusters.index=rows
    return df_models_in_clusters

"""
 * @summary give a list of the clusters (represented by their synonym) represented in a given number of models
 * @param {DataFrame(int)} df_models_in_clusters - a dataframe with in rows the models, in columns the cluster centroids, which represent the number of terms per cluster and per model.
 * @param {int} threshold - the threshold for the model number which present at least a term that belong to the cluster
 * @ret {list(string)} - the list of clusters (represented by their centroids) which appear at least in a number of models equal to threshold
"""
def more_present_clusters(df_models_in_clusters,threshold):
    nb_models_in_clusters=df_models_in_clusters.apply(lambda column: (column != 0).sum())
    selected_clusters=[]
    for synonym_cluster in nb_models_in_clusters.index:
        if nb_models_in_clusters[synonym_cluster]>=threshold:
            selected_clusters.append(synonym_cluster)
    return selected_clusters

"""
 * @summary give the relations in the models between two clusters
 * @param {string} centroid1 - the centroid of the first cluster
 * @param {string} centroid2 - the centroid of the second cluster
 * @param {list(Association)} associations - the list of all the associations in the chosen models
 * @param {list(Element)} classes - the list of all the elements in the chosen models
 * @param {int} mode - if 1, the terms linked are detailed in the resulting list
 * @ret {list(dict(string,?))} - a list of dictionaries containing the type of the relation, the model and the direction. If mode is 1, the client and the supplier Elements are included.
"""
def identify_links_cluster(centroid1,centroid2,associations,classes,mode=1):
    links_cluster=[]
    for assoc in associations:
        client=find_by_id(assoc.client,classes)
        supplier=find_by_id(assoc.supplier,classes)
        centroid_client=client.cluster
        centroid_supplier=supplier.cluster
        if centroid_client==centroid1 and centroid_supplier==centroid2:
            direction=1
            if assoc.type in [AssociationType.ASSOCIATION,AssociationType.ASSOCIATION_CLASS]:
                direction=0
            if mode==1:
                links_cluster.append({"type":assoc.type,"client":client,"supplier":supplier,"model":assoc.model,"direction":direction})
            else:
                links_cluster.append({"type":assoc.type,"model":assoc.model,"direction":direction})
        elif centroid_supplier==centroid1 and centroid_client==centroid2 and assoc.type in [AssociationType.ASSOCIATION,AssociationType.ASSOCIATION_CLASS]:
            if mode==1:
                links_cluster.append({"type":assoc.type,"client":supplier,"supplier":client,"model":assoc.model,"direction":0})
            else:
                links_cluster.append({"type":assoc.type,"model":assoc.model,"direction":0})
        elif centroid_supplier==centroid1 and centroid_client==centroid2:
            if mode==1:
                links_cluster.append({"type":assoc.type,"client":supplier,"supplier":client,"model":assoc.model,"direction":-1})
            else:
                links_cluster.append({"type":assoc.type,"model":assoc.model,"direction":-1})
    return links_cluster

"""
 * @summary check if two relations has the same type, the same direction and are in the same model
 * @param {dict(string,?)} link1 - a dictionary containing the type, direction and model of the relation at least
 * @param {dict(string,?)} link2 - a dictionary containing the type, direction and model of the relation at least
 * @ret {boolean} - a boolean indicating if the links are similar (same model, direction and type) or not
"""
def similar_links(link1,link2):
    return link1["type"]==link2["type"] and link1["model"]==link2["model"] and link1["direction"]==link2["direction"]

# To study redundant relations (i.e. relations with same type, same mode and direction)//Code qui étudie les relations redondantes (c'est-à-dire de même type, de même modèle et de même direction, qui impliquent souvent au moins un élément commun entre plusieurs relations)
# redundancies=[]
# c=0
# links_without_redundancies=[]
# for centroid1 in synonymes:
#     for centroid2 in synonymes:
#         # print(centroid1,centroid2)
#         links=identify_links_cluster(centroid1,centroid2, associations, classes)
#         for index_links in range(len(links)):
#             l1=links[index_links]
#             for l2 in links[index_links+1:]:
#                 if similar_links(l1,l2):
#                     redundancies.append({"l1":l1,"l2":l2})
#                     if l1["type"] not in [AssociationType.ENUMERATION]:
#                         c+=1
#                         print(l1["client"].name,",",l1["supplier"].name,l1["type"],l2["client"].name,",",l2["supplier"].name)
# print(c/len(redundancies))

"""
 * @summary replace the multiple occurrences of similar links (cf similar_links) by a link containing the same information, enriched with a weight which depend of the number of similar links found
 * @param {list(dict(string,?))} links - a list of links (represented by dictionaries containing the type, direction and model of a relation (at least))
 * @ret {list(dict(string,?))} - a list of links without redundancies (similar links) associated with a weigth
"""
def group_links(links):
    redundancies=[[] for l in links]
    for index_l1 in range(len(links)):
        l1=links[index_l1]
        for index_l2 in range(index_l1+1,len(links)):
            l2=links[index_l2]
            if similar_links(l1,l2):
                redundancies[index_l1].append(index_l2)
                redundancies[index_l2].append(index_l1)
    grouped_links=[]
    for index_l in range(len(links)):
        l=links[index_l]
        redundancies_l=redundancies[index_l]
        if redundancies_l==[]:
            l["weight"]=1
            grouped_links.append(l)
        else:
            if min(redundancies_l)>index_l:
                l["weight"]=1+(len(redundancies_l)+1)/len(links)
                grouped_links.append(l)
    return grouped_links

"""
 * @summary increment a counter of a specified value (weight) for the link type 
 * @param {AssociationType} link_type - the type of UML relation
 * @param {dict(AssociationType,float)} types_counter - a dictionary mapping the type of associations with their total weigth among the different models
 * @param {float} weigth - the weigth to add to the counter (in [1;2[ interval)
"""
def add_type(link_type,types_counter,weigth=1):
    if link_type in types_counter.keys():
        types_counter[link_type]+=weigth
    else:
        types_counter[link_type]=weigth

"""
 * @summary increment a counter to register the direction of a relation
 * @param {int,int} A - a counter of relations in natural sense and a counter of relations in the opposite sense
 * @param {float} z - the direction of the relation to take into account
 * @ret {int,int} - A, incremented (if the relation has no direction, the two counters are incremented)
"""
def add_coordinates(A,z):
    x1,y1=A
    x2,y2=1,0
    if z<0:
        x2=0
        y2=-1
    elif z==0:
        x2=1
        y2=-1
    return (x1+x2,y1+y2)

"""
 * @summary extract information about the relations linking two clusters : type, direction, number of models peresenting this kind of relation, total number of link among the models
 * @param {list(dict(string,?))} links_cluster - a list of dictionaries containing the type, the model and the direction of a relation (and, eventually, the client and the supplier Elements).
 * @ret {int,(int,int),dict(AssociationType,float),int} - 4 information : the total number of links passed in parameters, a double counting the (similar) relations in natural and inverses direction, a dictionary counting the number of relations per type, and the number of models represented in the list passed in parameters
"""
def information_of_links(links_cluster):
    direction=(0,0)
    types_counter=dict()
    models=[]
    for link in group_links(links_cluster):
        w=link["weight"]
        direction=add_coordinates(direction,link["direction"]*w)
        add_type(link["type"],types_counter,w)
        if link["model"] not in models:
            models.append(link["model"])
    return len(links_cluster),direction,types_counter,len(models)

"""
 * @summary make 4 matrix with the clusters in rows and columns, containing information about the relationships between each pair of cluster (cf information_of_link)
 * @param {list(Association)} associations - a list containing all the associations from the models
 * @param {list(Element)} classes - a list containing all the classes/elements from the models
 * @param {list(string)} centroids - the cluster centroids (clusters formed using the semantic information held by classes elements)
 * @ret {list(list(int)),list(list((int,int)),list(list(dict(AssociationType,float)),list(list(int))} - 4 matrix presenting respectively (per client and supplier cluster) : the total number of links passed in parameters, a double counting the (similar) relations in natural and inverses direction, a dictionary counting the number of relations per type, and the number of models represented in the list passed in parameters
"""
def link_tables(associations,classes,centroids):
    table_len=[]
    table_direction=[]
    table_types=[]
    table_models=[]
    for c1 in centroids:
        table_len_c1=[]
        table_direction_c1=[]
        table_types_c1=[]
        table_models_c1=[]
        for c2 in centroids:
            l,d,t,m=information_of_links(identify_links_cluster(c1, c2, associations, classes)) 
            table_len_c1.append(l)
            table_direction_c1.append(d)
            table_types_c1.append(t)
            table_models_c1.append(m)
        table_len.append(table_len_c1)
        table_direction.append(table_direction_c1)
        table_types.append(table_types_c1)
        table_models.append(table_models_c1)
    return table_len,table_direction,table_types,table_models

"""
 * @summary save a matrix in a csv file
 * @param {string} csv_name - the name of the file in which the data will be stored
 * @param {list(list(X))} table - one of the four table produced by link_tables
 * @param {list(string)} centroids - the cluster centroids, which will be used for the columns and rows titles
"""
def table_to_csv(csv_name,table,centroids):
    with open("Results/"+csv_name+".csv","w",encoding="utf-8") as csv_file:
        csv_file.write(";"+";".join(str(s) for s in centroids)+"\n")
        for index_table in range (len(table)):
            csv_file.write(centroids[index_table]+";"+';'.join(str(t) for t in table[index_table])+"\n")
    return

"""
 * @summary save a Dataframe in a csv file
 * @param {string} csv_name - the name of the file in which the data will be stored
 * @param {DataFrame(X)} df - the dataframe to save
"""
def df_to_csv(csv_name,df):
    df.to_csv(csv_name+'.csv', index=True)
    return

"""
 * @summary transform a term into an acceptable variable label
 * @param {string} name - the term
 * @ret {string} - the corresponding label
"""
def standardize(name):
    return name.lower().replace(" ","_")

"""
 * @summary transform a term into a class identifier for UML drawio file
 * @param {string} name - the term
 * @ret {string} - the corresponding identifier
"""
def identifier_class(name):
    return "cls_"+standardize(name)

"""
 * @summary transform two terms into an association identifier for UML drawio file
 * @param {string} name1 - the term hold by the first end of the association
 * @param {string} name2 - the term hold by the second end of the association
 * @ret {string} - the corresponding identifier
"""
def identifier_assoc(name1,name2):
    return "assoc_"+standardize(name1)+"_"+standardize(name2)

"""
 * @summary transform a term into an attribute identifier for UML drawio file. To reinforce the unicity of the identifier, a random integer is added to the identifier
 * @param {string} name - the term
 * @ret {string} - the corresponding identifier
"""
def identifier_attribute(name):
    return "attr_"+standardize(name)+str(randint(0,10000))

"""
 * @summary transform a term into an enumerated identifier for UML drawio file. To reinforce the unicity of the identifier, a random integer is added to the identifier
 * @param {string} name - the term
 * @ret {string} - the corresponding identifier
"""
def identifier_enum(name):
    return "enum_"+standardize(name)+str(randint(0,10000))

"""
 * @summary transform a term into a method identifier for UML drawio file. To reinforce the unicity of the identifier, a random integer is added to the identifier
 * @param {string} name - the term
 * @ret {string} - the corresponding identifier
"""
def identifier_method(name):
    return "meth_"+standardize(name)+str(randint(0,10000))

"""
 * @summary a function to be able to see which relations are most important in a drawio representation using different grey levels
 * @param {int} grey_level - the grey level
 * @ret {string} - the corresponding color, expressed in hexadecimal
"""
def rgb2hex(grey_level):
    return "#{:02x}{:02x}{:02x}".format(grey_level,grey_level,grey_level)

"""
 * @summary calculate a color (grey level) depending on a specified weigth (between 0 and 1)
 * @param {float} weigth - the weigth
 * @ret {string} - the corresponding color, expressed in hexadecimal
"""
def color(weigth):
    grey_level=int(255*(weigth))
    return rgb2hex(grey_level)

"""
 * @summary generate the first lines to write in a file to have a valid drawio
 * @ret {string} - a string containing the lines
"""
def preambule_drawio():
    return """<mxGraphModel dx="1426" dy="724" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
<root>
  <mxCell id="0" />
  <mxCell id="1" parent="0" />"""
 
"""
 * @summary write a "code" to generate a UML class in a drawio file
 * @param {string} name - the class/interface/enumerated label
 * @param {list(Element)} attributes - the attributes to represent in the class
 * @param {list(Element)} enumerated - the enumerated elements to represent in the class
 * @param {list(Element)} methods - the methods to represent in the class
 * @param {boolean} abstract - a boolean indicating if the class is abstract
 * @param {boolean} interface - a boolean indicating if the class is an interface
 * @ret {string} - a string containing the lines in drawio to describe the UML class
"""
def class_drawio(name,attributes=[],enumerated=[],methods=[],abstract=False,interface=False):
    id_class=identifier_class(name)
    drawio=""
    height=50
    width=110
    style="html=1;whiteSpace=wrap;"
    if interface:
        name="<<interface>>\n"+name
    if abstract:
        name="&lt;i&gt;"+name+"&lt;/i&gt;"
    if enumerated!=[]:
        style="swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=26;fillColor=none;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;"
        name="&lt;div&gt;&amp;lt;&amp;lt;enum&amp;gt;&amp;gt;&lt;/div&gt;&lt;div&gt;"+name+"&lt;/div&gt;"
        for e in enumerated:
            drawio+=f"""<mxCell id="{identifier_enum(e)}" parent="{id_class}" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;" value="{e}" vertex="1">
      <mxGeometry height="26" width="{width}" y="{height}" as="geometry" />
    </mxCell>"""
            height+=26
    if attributes!=[]:
        style="swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=26;fillColor=none;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;"
        height=26
        width=160
        for attribut in attributes:
            drawio+=f"""<mxCell id="{identifier_attribute(attribut)}" parent="{id_class}" style="text;strokeColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;" value="{attribut}" vertex="1">
      <mxGeometry height="26" width="{width}" y="{height}" as="geometry" />
    </mxCell>"""
        height+=26
    if methods!=[]:
        drawio+=f"""<mxCell id="{"separation_"+id_class}" parent="{id_class}" style="line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=right;points=[];portConstraint=eastwest;strokeColor=inherit;" value="" vertex="1">
      <mxGeometry height="8" width="{width}" y="{height}" as="geometry" />
    </mxCell>"""
        height+=8
        for method in methods:
            drawio+=f"""<mxCell id="{identifier_method(method)}" parent="{id_class}" style="text;strokeColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;" value="{method}" vertex="1">
      <mxGeometry height="26" width="{width}" y="{height}" as="geometry" />
    </mxCell>"""
            height+=26
    drawio=f"""<mxCell id="{id_class}" value="{name}" style="{style}" vertex="1" parent="1">
      <mxGeometry x="{randint(0,1426)}" y="{randint(0,724)}" width="{width}" height="{height}" as="geometry" />
    </mxCell>"""+drawio
    return drawio

"""
 * @summary write a "code" to generate a UML association in a drawio file. N.B. The code in the case of an association class is missing.
 * @param {string} name_end1 - the label of the first end of the relation
 * @param {string} name_end2 - the label of the second end of the relation
 * @param {AssociationType} assoc_type - the type of association
 * @param {float} weigth - a float between 0 and 1 to represent the association in a grey level which correspond to the number of models presenting this association.
 * @ret {string} - a string containing the lines in drawio to describe the UML relation
"""
def association_drawio(name_end1,name_end2,assoc_type=None,weigth=0):
    id_association=identifier_assoc(name_end1, name_end2)
    style=f"endArrow=none;html=1;edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor={color(weigth)};"
    
    # Gestion de la navigabilite
    if assoc_type==AssociationType.NAVIGABLE_ASSOCIATION:
        style="endArrow=cross;startArrow=open;endFill=0;startFill=0;endSize=8;startSize=10;html=1;rounded=0;"
    #Gestion des aggregations et compositions
    elif assoc_type==AssociationType.AGGREGATION:
        style="endArrow=diamondThin;endFill=0;endSize=24;html=1;rounded=0;"
    elif assoc_type==AssociationType.COMPOSITION:
        style="endArrow=diamondThin;endFill=1;endSize=24;html=1;rounded=0;"
    elif assoc_type==AssociationType.HERITAGE:
        style="endArrow=block;endSize=16;endFill=0;html=1;rounded=0;fontSize=12;curved=1;"
    elif assoc_type==AssociationType.ASSOCIATION_CLASS:
        raise Exception("I hoped it was too rare... Good luck to write the drawio lines to generate an association class (l. 420 - file 'link_matrix_into_drawio') !")
    elif assoc_type==AssociationType.DEPENDENCY:
        style="endArrow=open;endSize=12;dashed=1;html=1;rounded=0;"
    elif assoc_type==AssociationType.REALIZATION:
        style="endArrow=block;dashed=1;endFill=0;endSize=12;html=1;rounded=0;"
    
    drawio=f"""<mxCell id="{id_association}" edge="1" parent="1" source="{identifier_class(name_end1)}" style="{style}" target="{identifier_class(name_end2)}" value="">
      <mxGeometry relative="1" as="geometry">
        <mxPoint x="260" y="300" as="sourcePoint" />
        <mxPoint x="420" y="300" as="targetPoint" />
      </mxGeometry>
    </mxCell>"""
    return drawio

"""
 * @summary generate the final lines to write in a file to have a valid drawio
 * @ret {string} - a string containing the lines
"""
def end_drawio():
    return """  </root>
</mxGraphModel>"""

# def link_matrix_into_drawio(df_models,drawio_name,threshold):
#     nb_clusters=len(df_models.columns)
#     max_occurrences=df_models.max().max()
#     drawio_name+=str(threshold)
#     with open(drawio_name+".drawio","w") as output_file:
#         output_file.write(preambule_drawio())
#         for cluster_name in list(df_models.columns):
#             output_file.write(class_drawio(cluster_name))
#         for i in range(nb_clusters):
#             for j in range(i+1):
#                 nb_occurrences=df_models.loc[i].iloc[j]
#                 if nb_occurrences>threshold:
#                     output_file.write(association_drawio(df_models.columns[i], df_models.columns[j], weigth=1-nb_occurrences/max_occurrences))
#         output_file.write(end_drawio())
#     return drawio_name+".drawio"

"""
 * @summary get the majoritary direction of a relation between two clusters, if the difference between the weigth of the directions is higher than a threshold (which can be equal to 0).
 * @param {int,int} direction_vector - a negative number representing the weigth of the relations in inverse direction, a positive natural number to represent the weigth of the relations in natural direction
 * @param {float} threshold - the minimal difference to have to conclude about the direction of the relation - functionnality not used in GALA 2026 paper.
 * @ret {int} - an integer representing the majoritary direction (negative if it is inverse, positive if it is natural)
"""
def get_direction(direction_vector,threshold):
    client_to_supplier,supplier_to_client=direction_vector
    if abs(client_to_supplier-supplier_to_client)<=threshold:
        return 0
    return client_to_supplier+supplier_to_client

"""
 * @summary get the majoritary type of a relation between two clusters
 * @param {dict(AssociationType,float)} dict_type_nb - a dictionary mapping the type of relations with a weigth
 * @ret {ASSOCIATION_TYPE} - the relation type with the highest weigth
"""
def majoritary_type(dict_type_nb):
    default_type=AssociationType.ASSOCIATION
    nb_default_type=0
    for assoc_type,nb in dict_type_nb.items():
        if nb>nb_default_type:
            default_type,nb_default_type=assoc_type,nb
        elif nb==nb_default_type:
            default_type=AssociationType.ASSOCIATION
            nb_default_type=nb
    return default_type            

"""
 * @summary get the relations to represent in  the UML class diagram representing the pedago-ludic alignment
 * @param {DataFrame(int)} df_models - a dataframe with in rows and columns the clusters centroids, which contains the number of models presenting a relation between two clusters.
 * @param {list(list((int,int))} table_direction - a matrix presenting, per client and supplier cluster, a double counting the (similar) relations in natural and inverses direction
 * @param {list(list(dict(AssociationType,float))} table_type - a matrix presenting, for a given client and supplier cluster, a dictionary counting the number of relations per type
 * @param {float} threshold_models - the minimal number of models which has to present a relationship between two clusters to put the relation in the return dataframe
 * @param {float} threshold_direction - the minimal difference to have to conclude about the direction of the relation - functionnality not used in GALA 2026 paper.
 * @ret {DataFrame} - a dataframe listing the relations between two clusters which are represented in at least threshold_models by indicating the client cluster centroid, the supplier cluster centroid and the type of the relation
"""
def selection_links(df_models,table_direction,table_type,threshold_models,threshold_direction):
    selected_links=[]
    nb_clusters=len(table_direction)
    for index_column in range(nb_clusters):
        for index_row in range(index_column+1):
            index_df_column=df_models.columns[index_column]
            if df_models.loc[index_df_column].iloc[index_row]>threshold_models:
                direction_link=get_direction(table_direction[index_column][index_row],threshold_direction)
                if direction_link>=0:
                    selected_links.append([df_models.columns[index_column],df_models.columns[index_row],majoritary_type(table_type[index_column][index_row])])
                else:
                    selected_links.append([df_models.columns[index_row],df_models.columns[index_column],majoritary_type(table_type[index_column][index_row])])
    df_selected_links=pd.DataFrame(selected_links)
    if selected_links!=[]:
        df_selected_links.columns=["client","supplier","type"]
    return df_selected_links

"""
 * @summary write a drawio file to represent the set of associations passed in parameters and the corresponding classes
 * @param {DataFrame} df_associations - a dataframe listing the relations between two clusters to represent by indicating the client cluster centroid, the supplier cluster centroid and the type of the relation
 * @param {string} drawio_name - the name of the drawio file
 * @ret {string} - the complete name of the drawio_file - usefull to print and to know at which step is the compilation
"""
def association_dataframe_into_drawio(df_associations,drawio_name):
    clusters_included=dict()
    with open("Results/"+drawio_name+".drawio","w") as output_file:
        output_file.write(preambule_drawio())
        for index_current_association in range(len(df_associations.index)):
            assoc=df_associations.loc[index_current_association]
            client=assoc["client"]
            supplier=assoc["supplier"]
            type_assoc=assoc["type"]
            if client not in clusters_included.keys():
                clusters_included[client]={attr:[],meth:[],enum:[]}
            if supplier not in clusters_included.keys():
                clusters_included[supplier]={attr:[],meth:[],enum:[]}
            if type_assoc==AssociationType.ATTRIBUTE:
                clusters_included[client][attr].append(supplier)
            elif type_assoc==AssociationType.ENUMERATION:
                clusters_included[client][enum].append(supplier)
            elif type_assoc==AssociationType.METHOD:
                clusters_included[client][meth].append(supplier)
            else:
                output_file.write(association_drawio(client, supplier, type_assoc))
        for name,content in clusters_included.items():
            output_file.write(class_drawio(name,content[attr],content[enum],content[meth]))
        output_file.write(end_drawio())
    return drawio_name+".drawio"

"""
 * @summary count the number of models taken into account in a set
 * @param {int} identifier - the identifier of the model set
 * @ret {int} - the number of models in the set represented by the identifier
"""
def get_nb_models(identifier):
    return bin(identifier).count('1')

# Generate the drawio files for different thresholds, and store the tables summarizing the relations information in csv files
nb_models=get_nb_models(identifier_selected_models)
csv=["nb_associations","direction","types","nb_models"]
df_models_in_clusters=identify_models_in_clusters(classes)
print(df_models_in_clusters)
df_to_csv("models_in_clusters", df_models_in_clusters)
for threshold in range((nb_models+1)//2,nb_models):  
    selected_centroids=more_present_clusters(df_models_in_clusters, threshold)
    tables=link_tables(associations,classes,selected_centroids)
    table_len,table_direction,table_type,table_models=tables
    df_models=pd.DataFrame(table_models)
    df_models.columns=[syn for syn in selected_centroids]
    df_models.index=[syn for syn in selected_centroids]
    print(df_models)
    
    threshold_direction=0
    for threshold_models in range(2,7):
        set_of_selected_links=selection_links(df_models, table_direction, table_type, threshold_models, threshold_direction)
        print(association_dataframe_into_drawio(set_of_selected_links, f"malp{identifier_selected_models}_links{threshold_models}_clusters{threshold}"))

threshold=0
selected_centroids=more_present_clusters(df_models_in_clusters, threshold)
tables=link_tables(associations,classes,selected_centroids)
table_len,table_direction,table_type,table_models=tables
for no_table in range(len(tables)):
    table_to_csv(csv[no_table]+str(identifier_selected_models),tables[no_table],selected_centroids)

print(f"Calculs effectués en {time.time()-t0} s")
