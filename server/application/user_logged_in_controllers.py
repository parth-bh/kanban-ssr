from flask import Flask, request, session
from flask import render_template, send_file
from flask import current_app as app
from flask import Flask, request, flash, url_for, redirect, render_template
from flask import current_app as app

from .database import db
from .models import *

import pandas as pd
from .functions import *

from datetime import date



# -------------------------------------------------USER LOGGED IN PART ----------------------------------------


@app.route("/<user_name>", methods=["GET", "POST"])
def user_logged_in(user_name):

    # user must be logged.  
	if 'user_name' not in session:  
		return redirect(url_for('home'))

	user_query = User.query.filter_by(user_name= user_name).first()

	if user_query is None:
		return render_template("error_handling.html")

    #  call data from function.py
	user_data, user_list = ExtractUserData_UserList_by_UserName(user_name)

	if request.method == "GET":
		return render_template("user_logged_in.html", user=user_name, data=user_data, user_list=user_list)

	elif request.method == "POST":
		form = request.form
        # if user selected the existing list then render the page below manner.
		if "selected_list" in form.keys():
			user_list_df = Extract_List_Data(user_name)
			selected_list_id = list(user_list_df[user_list_df.list_name==form['selected_list']].list_id)[0]
			return redirect(url_for('user_selected_list', user_name=user_name, selected_list_id=selected_list_id))


						




# -------------------------------------------------When User Select the list  ----------------------------------------


@app.route("/<user_name>/<selected_list_id>", methods=["GET", "POST"])
def user_selected_list(user_name, selected_list_id):

    # user must be logged.  
	if 'user_name' not in session:  
		return redirect(url_for('home'))

	user_data, user_list = ExtractUserData_UserList_by_UserName(user_name)
	user_list_df = Extract_List_Data(user_name)
	
	user_list_df = Extract_List_Data(user_name)
	selected_list = list(user_list_df[user_list_df.list_id==int(selected_list_id)].list_name)[0]

	data=user_data[user_data.list_name == selected_list]

	progress_df = data[data.completion_status=="In-Progress"]
	not_completed_df = data[data.completion_status=="Not-Completed"]
	completed_df = data[data.completion_status=="Completed"]

	n_completed = completed_df.shape[0]
	n_not_completed = not_completed_df.shape[0]
	n_progress = progress_df.shape[0]

	n_data = data.shape[0]

	return render_template("user_logged_in.html", user=user_name, progress_df=progress_df,
							not_completed_df=not_completed_df, completed_df=completed_df,
							 user_list=user_list, selected_list=selected_list, n_data=n_data,
							 n_completed=n_completed, n_progress=n_progress, n_not_completed=n_not_completed)
	







# -------------------------------------------------When User adding a list ----------------------------------------


@app.route("/<user_name>/add_list", methods=["GET", "POST"])
def user_adding_list(user_name):

    # user must be logged.  
	if 'user_name' not in session:  
		return redirect(url_for('home'))

	if request.method == "POST":
		form = request.form

		user_data, user_list = ExtractUserData_UserList_by_UserName(user_name)
	  	# if user added a new list, then add the list name in the database
		if "add_list" in form.keys():
			if form["add_list"] in user_list:
				error = f'List name "{form["add_list"]}" is already exist, please try with other name'
				return render_template("error_handling.html", error=error, user=user_name)
			else:
				try:
					new_entry = ListDetails(list_name=form["add_list"], user_name=user_name)
					db.session.add(new_entry)
					db.session.commit()

					# call data again as new entry is added in the database.
					selected_list = form["add_list"]  # new added list is going to be the selected list.
					user_list_df = Extract_List_Data(user_name)
					selected_list_id = list(user_list_df[user_list_df.list_name==selected_list].list_id)[0]

					return redirect(url_for('user_selected_list', user_name=user_name, selected_list_id=selected_list_id))
				except:
					db.session.rollback()
					error = "Something is wrong while initiating to the database, please try later or contact to admin."
					return render_template("error_handling.html", error=error, user=user_name)
		else:
			return render_template("error_handling.html")




# -------------------------------------------------When User deleting a list ----------------------------------------

@app.route("/<user_name>/delete_list", methods=["GET", "POST"])
def user_deleting_list(user_name):

    # user must be logged.  
	if 'user_name' not in session:  
		return redirect(url_for('home'))

	if request.method == "POST":
		form = request.form
		user_data, user_list = ExtractUserData_UserList_by_UserName(user_name)
	    # if user added a new list, then add the list name in the database
		if form["deleting_list"] not in user_list:
			error = f"Something goes wrong, please try later."
			return render_template("error_handling.html", error=error, user=user_name)
		else:
			try:
				# delete from the MainDetails Schema, delete all card detaiks for that particular list
				user_list_df = Extract_List_Data(user_name)
				deleting_list = form['deleting_list']

# ****check below line later, is this applicable for all or not

				deleting_list_id = list(user_list_df[user_list_df.list_name==deleting_list].list_id)[0]
				deleting_query_MainDetails = MainData.query.filter_by(list_id=deleting_list_id, user_name=user_name).all()
				
				if deleting_query_MainDetails:
					for iter in deleting_query_MainDetails:
						db.session.delete(iter)

				# delete from the ListDetails Schema, delete list
				deleting_query_ListDetails = ListDetails.query.filter_by(list_name=form["deleting_list"], user_name=user_name).all()
				if deleting_query_ListDetails:
					for iter in deleting_query_ListDetails:
						db.session.delete(iter)

				db.session.commit()
				return redirect(url_for('user_logged_in', user_name=user_name))
				
			except:
				db.session.rollback()
				error = "Something is wrong while initiating to the database, please try later or contact to admin."
				return render_template("error_handling.html", error=error, user=user_name)
	else:
		return render_template("error_handling.html")





# -------------------------------------------------When User edit the list name----------------------------------------

@app.route("/<user_name>/edit_list", methods=["GET", "POST"])
def user_edit_list(user_name):

    # user must be logged.  
	if 'user_name' not in session:  
		return redirect(url_for('home'))

	if request.method == "POST":
		form = request.form
		user_data, user_list = ExtractUserData_UserList_by_UserName(user_name)
	    # if user added a new list, then add the list name in the database
	    # if user edit_list is already in the user_list, then gave error because we want the list_name as unique
	    # but one thing notice here is that, edit_list is not same as that we select the list_name
		if form["edit_list"] in user_list and form["edit_list"] != form["selected_list"]:
			error = f'List name "{form["edit_list"]}" is already exist, please try with other name'
			return render_template("error_handling.html", error=error, user=user_name)
		else:
			try:
				edit_query_ListDetails = ListDetails.query.filter_by(list_name=form["selected_list"], user_name=user_name)
				for iter in edit_query_ListDetails:
					iter.list_name = form["edit_list"]

				db.session.commit()

				selected_list = form["edit_list"]
				user_list_df = Extract_List_Data(user_name)
				selected_list_id = list(user_list_df[user_list_df.list_name==selected_list].list_id)[0]

				return redirect(url_for('user_selected_list', user_name=user_name, selected_list_id=selected_list_id))

			except:
				db.session.rollback()
				error = "Something is wrong while initiating to the database, please try later or contact to admin."
				return render_template("error_handling.html", error=error, user=user_name)








# -------------------------------------------------When User Edit the Card/Tasks ----------------------------------------


@app.route("/<user_name>/edit_card", methods=["GET", "POST"])
def user_edit_card(user_name):

    # user must be logged.  
	if 'user_name' not in session:  
		return redirect(url_for('home'))

	form = request.form

	if request.method == "POST":
		# edit_card means when a user request to edit the card details 
		# and we have to give them the form for editing the details of cards.
		# modify card is when user give the new details of particular card.

		if "edit_card" in form.keys() and "modify_card" not in form.keys():
			user_data, user_list = ExtractUserData_UserList_by_UserName(user_name)
			id_query = MainData.query.filter_by(id=form['id']).first()
			selected_list = form['list_name']
			selected_title = id_query.title
			data = user_data[(user_data.list_name==selected_list) & (user_data.title==selected_title)]
			data = data.reset_index(drop=True)
			# if we don't reset the index, then this take the index of older dataframe where it was extracted from.
			return render_template("edit_card_details.html", data=data, user_list=user_list, user=user_name, selected_list=selected_list)
		
		elif "modify_card" in form.keys() and form['modify_card']=="modify":
			try:
				user_list_df = Extract_List_Data(user_name)


				mark_as_complete = True if form['mark_as_complete'] == "1" else False

				# update the completion_date if mark is True
				today = date.today()	
				completion_date = today if form['mark_as_complete'] == "1" else None

				# now also edit the list name from MainData
				query = MainData.query.filter_by(id=form['id']).first()
				prev_selected_list = form['selected_list']
				prev_selected_list_id = list(user_list_df[user_list_df.list_name==prev_selected_list].list_id)[0]

				new_list_name = form['list_name']
				new_list_id = list(user_list_df[user_list_df.list_name==new_list_name].list_id)[0]

				# if by chance user change the list_name, then new_list_name should be in the form['list_name']
				# and previous list_name is in prev_selected_list
				query.list_id = new_list_id
				query.title = form['title']
				query.content = form['content']
				query.deadline = form['deadline']
				query.mark_as_complete = mark_as_complete
				query.completion_date = completion_date
				
				# now commit
				db.session.commit()
				selected_list = form['list_name']
				user_list_df = Extract_List_Data(user_name)
				selected_list_id = list(user_list_df[user_list_df.list_name==selected_list].list_id)[0]

				return redirect(url_for('user_selected_list', user_name=user_name, selected_list_id=selected_list_id))
			
			except:
				db.session.rollback()
				error = "Something is wrong while initiating to the database, please try later or contact to admin."
				return render_template("error_handling.html", error=error, user=user_name)
		else:
			return render_template("error_handling.html")







# -------------------------------------------------When User Delete the Card/Tasks ----------------------------------------

# there will be no confirmation for deleting the cards.
# but there will be confirmation for deleting the List, if we delete the whole lists.

@app.route("/<user_name>/delete_card", methods=["GET", "POST"])
def user_delete_card(user_name):

    # user must be logged.  
	if 'user_name' not in session:  
		return redirect(url_for('home'))

	if request.method == "POST":
		try:
			form = request.form
			delete_query = MainData.query.filter_by(id=form['id']).first()
			db.session.delete(delete_query)
			db.session.commit()

			selected_list = form['list_name']
			user_list_df = Extract_List_Data(user_name)
			selected_list_id = list(user_list_df[user_list_df.list_name==selected_list].list_id)[0]

			return redirect(url_for('user_selected_list', user_name=user_name, selected_list_id=selected_list_id))
		except:
			db.session.rollback()
			error = "Something is wrong while initiating to the database, please try later or contact to admin."
			return render_template("error_handling.html", error=error, user=user_name)
	else:
		return render_template("error_handling.html")





# -------------------------------------------------When User Add the Card/Tasks ----------------------------------------


@app.route("/<user_name>/add_card", methods=["GET", "POST"])
def user_add_card(user_name):

    # user must be logged.  
	if 'user_name' not in session:  
		return redirect(url_for('home'))

	form = request.form
	if request.method == "POST":
	# this function will run only for post method, if a query raise for adding the new card, then add_card variable has value
	# and new_card varaible has details when user fill the details of new card.

#when apply for the adding the new card or task
		if "add_card" in form.keys() and "new_card" not in form.keys():
			user_data, user_list = ExtractUserData_UserList_by_UserName(user_name)
			selected_list = form['list_name']
			form = request.form
			return render_template("new_card_details.html", user_list=user_list, user=user_name, selected_list=selected_list)
		
# when card details will send to the server
		elif "new_card" in form.keys() and form['new_card'] == "save":
			try:
				user_list_df = Extract_List_Data(user_name)
				selected_list = form['list_name']
				selected_list_id = list(user_list_df[user_list_df.list_name==selected_list].list_id)[0]
				

				mark_as_complete = True if form['mark_as_complete'] == "1" else False

				today = date.today()
				completion_date = today if form['mark_as_complete'] == "1" else None

				add_query = MainData(user_name=user_name, list_id=selected_list_id, 
					title=form['title'], content=form['content'], 
					deadline=form['deadline'], mark_as_complete=mark_as_complete,
					start_date=today, completion_date=completion_date)	

				db.session.add(add_query)
				db.session.commit()
				selected_list = form['list_name']
				user_list_df = Extract_List_Data(user_name)
				selected_list_id = list(user_list_df[user_list_df.list_name==selected_list].list_id)[0]

				return redirect(url_for('user_selected_list', user_name=user_name, selected_list_id=selected_list_id))

			except:
				db.session.rollback()
				error = "Something is wrong while initiating to the database, please try later or contact to admin."
				return render_template("error_handling.html", error=error, user=user_name)
		else:
			return render_template("error_handling.html")







# -------------------------------------------------USER SETTINGS PART ----------------------------------------


@app.route("/<user_name>/settings")
def user_settings(user_name):

    # user must be logged.  
	if 'user_name' not in session:  
		return redirect(url_for('home'))

	user_query = User.query.filter_by(user_name=user_name).first()
	return render_template("settings.html", user_query = user_query, user=user_name)


@app.route("/<user_name>/export") # this is a job for GET, not POST
def export(user_name):
    # user must be logged.  
	if 'user_name' not in session:  
		return redirect(url_for('home'))

	# download the data and store it in static folder
	user_data, user_list = ExtractUserData_UserList_by_UserName(user_name)
	user_data.to_csv("outputs/kanban_data.csv")

	return send_file('outputs/kanban_data.csv',download_name='kanban.csv')




