from flask import Flask , render_template , request , redirect , url_for , session
from flask_sqlalchemy import SQLAlchemy
from models.model import *
import os

current_dir = os.path.dirname(os.path.abspath(__file__)) #just to make it work in case we change the directory

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
os.path.join(current_dir, 'database.sqlite3')

db.init_app(app) #connects our database to the app part of the flask
app.app_context().push()    #basically like a manager that manages the app context and pushes it to the app. database wont be created without this line.





if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
