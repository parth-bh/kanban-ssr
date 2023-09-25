from flask import Flask, session
import os
from application.database import db

app=None

def create_app():
    app = Flask(__name__)
    path = f"{os.getcwd()}/db_directory/testdb2.sqlite3"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + path
    db.init_app(app)
    return app

app=create_app()
app.app_context().push()

from application.controllers import *
from application.user_logged_in_controllers import *
from application.summary_controllers import *


if __name__ == "__main__":
	app.debug = True
	app.run()
