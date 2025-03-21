#flask and sqlalchemy imports
from flask import Flask , render_template  as rt , request , redirect , url_for , session
from flask_sqlalchemy import SQLAlchemy

#imports from model.py
from models.model import *



#random imports for other things
import os

current_dir = os.path.dirname(os.path.abspath(__file__)) #just to make it work in case we change the directory

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
os.path.join(current_dir, 'database.sqlite3')

db.init_app(app) #connects our database to the app part of the flask
app.app_context().push()    #basically like a manager that manages the app context and pushes it to the app. database won't be created without this line.



#this import is here because we need to import the routes after the app is created
#I tried doing it before that and it crashed.
#this issue is called circular import issue. VERY IMPORTANT!!!!!
#imports from controller.py
from controllers.controller import *


# Set secret key using secrets module
#its important to create secure sessions. Some cache related stuffs.
import secrets
app.secret_key = secrets.token_hex(16)



if __name__ == '__main__':
    db.create_all() #creates all the database

    super_user = User.query.filter_by(username = 'admin_Niraj').first()
    if super_user is None:
        admin = User(fullname = 'Niraj' , email = 'admin@123' , username = 'admin_Niraj' , password = '7548' , type = 'admin')
        db.session.add(admin)
        db.session.commit()
    # db.commit_all() #commits the changes to the database
    app.run(debug=True)
