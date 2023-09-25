from .database import db
from .models import *

import numpy as np
import pandas as pd
from datetime import date  
import datetime 





def Extract_List_Data(user_name):
    # user_list will be the list of list_names that is created by the particular user_name

    query = ListDetails.query.filter_by(user_name=user_name).all()

    user_list_dict = {"list_id":[],"user_name":[],"list_name":[]}
    for iter in query:
        user_list_dict['list_id'].append(iter.list_id)
        user_list_dict['user_name'].append(iter.user_name)
        user_list_dict['list_name'].append(iter.list_name)

    user_list_df = pd.DataFrame.from_dict(user_list_dict)
    return user_list_df





def ExtractUserData_UserList_by_UserName(user_name):
	# now extract the data.

    query1 = MainData.query.filter_by(user_name=user_name).all()

    user_data_dict = {"id":[],"user_name":[],"list_id":[], "title":[], "content":[], 
                        "deadline":[], "mark_as_complete":[],
                        "start_date":[], "completion_date":[]}
    for iter in query1:
        user_data_dict['id'].append(iter.id)
        user_data_dict['user_name'].append(iter.user_name)
        user_data_dict['list_id'].append(iter.list_id)
        user_data_dict['title'].append(iter.title)
        user_data_dict['content'].append(iter.content)
        user_data_dict['deadline'].append(iter.deadline)
        user_data_dict['mark_as_complete'].append(iter.mark_as_complete)
        user_data_dict['start_date'].append(iter.start_date)
        user_data_dict['completion_date'].append(iter.completion_date)
        

    # list_name is not addd in the user_data, this part where we add the list_name is added later
    # because got an error when we set the primary key as an list_id instead of list_name.
    # list_id should be primary key instead of list_name because     
    user_data = pd.DataFrame.from_dict(user_data_dict)
    user_list_df = Extract_List_Data(user_name) 
    list_name = []
    for elem in user_data.list_id:
        name = list(user_list_df[user_list_df.list_id==int(elem)].list_name)[0]
        list_name.append(name)

    user_data['list_name'] = list_name


    # now create the one column for giving the completion_status 

    completion_status = []
    today = date.today()

    for start_iter, deadline_iter, completion_iter in zip(user_data['start_date'], user_data['deadline'], user_data['completion_date']):

        deadline_iter = datetime.datetime.strptime(deadline_iter, '%Y-%m-%d').date() 
        completion_iter = datetime.datetime.strptime(completion_iter, '%Y-%m-%d').date() if completion_iter is not None else None

        if (completion_iter == None) and (deadline_iter >= today):
            completion_status.append("In-Progress")
        elif (completion_iter == None) and (deadline_iter < today):
            completion_status.append("Not-Completed")
        elif (completion_iter != None) and (deadline_iter < completion_iter):
            completion_status.append("Not-Completed")
        elif (completion_iter != None) and (deadline_iter >= completion_iter):
            completion_status.append("Completed")
        else:
            completion_status.append(None)

    user_data['completion_status'] = completion_status

    # now extract the list here that belongs to the particular user.


    query2 = ListDetails.query.filter_by(user_name=user_name).all()

    user_list = []
    for iter in query2:
        user_list.append(iter.list_name)

    return user_data, user_list











