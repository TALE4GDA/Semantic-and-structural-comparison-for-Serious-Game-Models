# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 10:26:10 2026

@author: madeleine.valat
"""

import tkinter as tk
import os

from tools import files,identifier_models,global_path

path=global_path+"StructuralComparison/"

window = tk.Tk()
window.title('My Window')

"/!\ To use this code, you have to download draw.io app (https://github.com/jgraph/drawio-desktop/releases/tag/v31.1.8) and to make sure that the .drawio files are opened by this app by default."

"""
 * @summary open the .drawio file which correspond to the parameters set in the tkinter window
"""
def open_diagram():
    model_list=[]
    for name_model,var in model_vars.items():
        if var.get()==1:
            model_list.append(name_model)
    identifier=identifier_models(model_list)
    threshold_links=nb_links_scale.get()
    threshold_clusters=nb_clusters_scale.get()
    file_path=path+f"malp{identifier}_links{threshold_links}_clusters{threshold_clusters}.drawio"
    os.startfile(file_path)

model_frame = tk.Frame(window, bg="lightblue", width=200, height=100, bd=3, relief=tk.RIDGE)
model_frame.grid(column=0,row=0,rowspan=10)
            
model_vars=dict()
for name_model in files:
    model_vars[name_model]=tk.IntVar()
    c = tk.Checkbutton(model_frame, text=name_model,variable=model_vars[name_model], onvalue=1, offvalue=0)
    c.pack()

label = tk.Label(window,text="Threshold models")
label.grid(column=1,row=0)
nb_clusters_var = tk.IntVar()
nb_clusters_scale = tk.Scale( window, variable = nb_clusters_var,from_=0,to=len(model_vars))
nb_clusters_scale.grid(column=1,row=1)

label = tk.Label(window,text="Threshold links")
label.grid(column=1,row=2)
nb_links_var = tk.IntVar()
nb_links_scale = tk.Scale( window, variable = nb_links_var,from_=0,to=len(model_vars))
nb_links_scale.grid(column=1,row=3)

label = tk.Label(window,text="Threshold direction")
label.grid(column=1,row=4)
direction_spinbox = tk.Spinbox(window, from_=0, to=2)
direction_spinbox.config(state="normal", cursor="hand2", bd=3, justify="center", wrap=True)
direction_spinbox.grid(column=1,row=5)
direction_threshold=direction_spinbox.get()

upload_button = tk.Button(window, text="Generate diagram", command=open_diagram)
upload_button.grid(column=2,row=10)
 
window.mainloop()