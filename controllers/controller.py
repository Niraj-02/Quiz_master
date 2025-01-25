#importing flask things
from flask import render_template as rt

#app import from app.py
from app import app

#model import from model.py
from models.model import *



@app.route('/' , methods = ['GET' , 'POST'])
def home():
    print("route accessed")
    return rt("home.html")


@app.route('/login' , methods = ['GET' , 'POST'])
def login():
    return rt("login.html")

@app.route('/register' , methods = ['GET' , 'POST'])
def register():
    return rt("register.html")


@app.route('/gpt' , methods = ['GET' , 'POST'])
def gpt():
    return rt("home2.html")