from flask import Flask, request, session
from flask import render_template, send_file
from flask import current_app as app
from flask import Flask, request, url_for, redirect, render_template
from flask import current_app as app

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
import io

from .database import db
from .models import *

import pandas as pd
import numpy as np
from .functions import *

from datetime import date
import datetime




# ------------------------------------------------Some Useful Functions for plotting Graphs---------- -----------------------





def plot_for_each_list(x, y, list_name_iter):
    plt.figure(figsize=(10,5))
    plt.barh(x, y,height=0.5, color=["red", 'green', 'blue'])
    plt.xlabel(f"Number of Tasks in '{list_name_iter}'", fontsize=18)
    plt.ylabel('Completion Status', fontsize=14)
    plt.title(f"{y[-1]}/{sum(y)} Completed, {y[1]}/{sum(y)} Progress, {y[0]}/{sum(y)} Not-Completed", loc="center", fontsize=20)
    plt.yticks(rotation = 90)
    for i in range(len(y)):
        plt.annotate(str(y[i]), xy=(y[i],x[i]), ha='left', va='bottom', fontsize=18)

    for s in ['right', 'left']:
        plt.gca().spines[s].set_visible(False)
    list_name_iter = "static/img/"+list_name_iter
    return plt.savefig(list_name_iter)




def date_vs_task_line_graph(data):
    x=[]
    for i in range(7): # we are going to take the 7-days data
        var = (datetime.datetime.today() - datetime.timedelta(days=i)).date()
        x.append(str(var))
    x = x[::-1]
    y=[]
    for i in x:
        var = data[data.start_date==i].shape[0]
        y.append(var)
    plt.figure(figsize=(6,6))
    plt.plot(x, y)
    plt.xlabel('Date:When Task is Created', fontsize=15)
    plt.ylabel('Number of Task', fontsize=15)
    plt.title("Number of Task Created in Each Day", loc="center", fontsize=20)
    plt.xticks(rotation=10)
    for i in range(len(y)):
        plt.annotate(str(y[i]), xy=(x[i],y[i]), ha='left', va='bottom', fontsize=20)
    for s in ['right', 'left']:
        plt.gca().spines[s].set_visible(False)
    
    return plt.savefig("static/img/date_vs_task_line_graph")

def completed_task_vs_date_line_graph(data):
    x=[]
    for i in range(7): # we are going to take the 7-days data
        var = (datetime.datetime.today() - datetime.timedelta(days=i)).date()
        x.append(str(var))
    x = x[::-1]
    y=[]
    for i in x:
        var = data[(data.completion_date==i) & (data.completion_status=='Completed')].shape[0]
        y.append(var)
    plt.figure(figsize=(6,6))
    plt.plot(x, y)
    plt.xlabel('Date: When Task is completed', fontsize=15)
    plt.ylabel('Number of Task', fontsize=15)
    plt.title("Number of Task Completed in Each Day", loc="center", fontsize=20)
    plt.xticks(rotation=10)
    for i in range(len(y)):
        plt.annotate(str(y[i]), xy=(x[i],y[i]), ha='left', va='bottom', fontsize=20)
    for s in ['right', 'left']:
        plt.gca().spines[s].set_visible(False)
    
    return plt.savefig("static/img/completed_task_vs_date_graph")


    





# -------------------------------------------------when user clicked the summary page -----------------------



@app.route("/<user_name>/summary", methods=["GET", "POST"])
def summary(user_name):

    # user must be logged.  
    if 'user_name' not in session:  
        return redirect(url_for('home'))


    user_data, user_list = ExtractUserData_UserList_by_UserName(user_name)
    list_details = user_data['list_name'].value_counts()
    n_task = list_details.sum()     # number of tasks
    n_list = len(user_list)   # number of list


	# now creating the completion status graph for each list 

    empty_task_list_name = []

    for list_name_iter in user_list:
        temp_data = user_data[user_data.list_name==list_name_iter]
        temp_dict = temp_data.completion_status.value_counts().to_dict()
        if temp_dict:
            x=["Not-Completed", "In-Progress", "Completed"]
            y=[] 
            for status in x:
                if status in temp_dict.keys():
                    y.append(temp_dict[status])
                else:
                    y.append(0)	
            plot_for_each_list(x, y, list_name_iter)
        else:
            empty_task_list_name.append(list_name_iter)

	# now creating the completion status graph for overall data


    temp_dict = user_data.completion_status.value_counts().to_dict()
    no_data = False
    if temp_dict:
        x=["Not-Completed", "In-Progress", "Completed"]
        y=[]
        for status in x:
            if status in temp_dict.keys():
                y.append(temp_dict[status])
            else:
                y.append(0)	
        plot_for_each_list(x, y, "Including_All_List")

    else:
        no_data = True
    user_list_non_empty = [i+".png" for i in set(user_data['list_name'])]


    # now create the line graph where number of task created in each day is shown.
    date_vs_task_line_graph(user_data)
    completed_task_vs_date_line_graph(user_data)

    empty_task_n_list = len(empty_task_list_name)

    return render_template("summary.html", user=user_name, n_list=n_list, empty_task_n_list=empty_task_n_list,
		n_task=n_task, user_list_non_empty=user_list_non_empty, list_details=list_details, user_list=user_list,
		empty_task_list_name=empty_task_list_name, no_data=no_data)


