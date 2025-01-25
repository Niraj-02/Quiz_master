#flask and sqlalchemy imports
from flask import Flask , render_template  as rt , request , redirect , url_for , session
from flask_sqlalchemy import SQLAlchemy

#imports from model.py
from models.model import *



#random immports for other things
import os

current_dir = os.path.dirname(os.path.abspath(__file__)) #just to make it work in case we change the directory

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
os.path.join(current_dir, 'database.sqlite3')

db.init_app(app) #connects our database to the app part of the flask
app.app_context().push()    #basically like a manager that manages the app context and pushes it to the app. database wont be created without this line.



#this import is here because we need to import the routes after the app is created
#I tried doing it before that and it crashed.
#this issue is called circular import issue. VERY IMPORTANT!!!!!
#imports from controller.py
from controllers.controller import *

if __name__ == '__main__':
    db.create_all() #creates all the database
    app.run(debug=True)
