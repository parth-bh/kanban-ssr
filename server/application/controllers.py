from flask import Flask, request, session
from flask import render_template
from flask import current_app as app
from flask import Flask, request, flash, url_for, redirect, render_template
from flask import current_app as app

from .database import db
from .models import *

import os

import pandas as pd
from .functions import *

app.config['SECRET_KEY'] = os.urandom(24)

# creating the secret key that is 24 character long
# this secret key stored on server as well as stored on the client side as a cookie.
# if secret key will expire in any side, then the session will be deactivated for the client.
# and then user have to login again.


# -------------------------------------------------When user open the app ----------------------------------------


@app.route("/", methods=["GET"])
def home():

    #if by chance user typed this url and user was already logged in, then redirect to the user page.
    if 'user_name' in session:
        return redirect(url_for('user_logged_in', user_name = session['user_name']))
    else:
        return render_template("home.html")



# -------------------------------------------------When User login, so verify their details.----------------------------------------


@app.route("/login_validation", methods=["GET", "POST"])
def login_validation():

    #if by chance user typed this url and user was already logged in, then redirect to the user page.
    if 'user_name' in session:
        return redirect(url_for('user_logged_in', user_name = session['user_name']))

    if request.method == "GET":
        return redirect(url_for('home'))

    if request.method == "POST":
        form = request.form
        query = User.query.filter_by(user_name=form["user_name"]).first()
        user_name_status, password_status = None, None

        # check the user name and password credientials will be matching with the database present or not
        # and respond accordingly.

        if query is None:
            error = f"User: '{form['user_name']}' doesn't exist. Please register yourself."
            return render_template("home.html", error=error)

        else:
            if query.password != form['password']:
                error = f"Incorrect Password. Please try again."
                return render_template("home.html", error=error)

            elif query.password == form["password"]:
                session['user_name'] = query.user_name
                return redirect(url_for('user_logged_in', user_name=form["user_name"]))






# -------------------------------------------------When User SignUp / Register ----------------------------------------


@app.route("/signup", methods=["GET", "POST"])
def signup():

    #if by chance user typed this url and user was already logged in, then redirect to the user page.
    if 'user_name' in session:
        return redirect(url_for('user_logged_in', user_name = session['user_name']))
    
    if request.method=="GET":
        return render_template("signup.html")
    
    if request.method=="POST":
        form = request.form
        user_name_query = User.query.filter_by(user_name=form["user_name"]).first()
        email_query = User.query.filter_by(email=form["email"]).first()
        
        #user_name is primary key and email would be unique, according to the database specifications.

        if user_name_query is not None:
            error = f"User: '{form['user_name']}' is already exist. Please register with other User Name."
            return render_template("signup.html", error = error)

        elif email_query is not None:
            error = f"Email: '{form['email']}' is already exist. Please try with other Email."
            return render_template("signup.html", error = error)
        
        try:
            new_entry = User(email=form["email"], user_name=form["user_name"], password=form["password"])
            db.session.add(new_entry)
            db.session.commit()
            message = f"User: '{form['user_name']}' Successfully Created. You can Login."
            return render_template("signup.html", message=message)

        except:
            db.session.rollback()
            return render_template("error_handling.html")






# -------------------------------------------------When User LogOut ----------------------------------------


@app.route('/logout')
def logout():
    if 'user_name' in session:
        session.pop('user_name')
        return redirect(url_for("home"))
    return redirect(url_for("home"))
        











