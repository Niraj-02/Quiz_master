#importing flask things
from flask import render_template as rt , request , redirect , url_for , session

#app import from app.py
from app import app

#model import from model.py
from models.model import *



@app.route('/' , methods = ['GET' , 'POST'])
def home():
    print("route accessed")
    return rt("home.html")

# route for login

@app.route('/login' , methods = ['GET' , 'POST'])
def login():
    if request.method == 'GET':
        return rt("login.html")  #essentially same as rt("login.html")
    
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # query to check if user exists
        user = User.query.filter_by(username = username).first()

        #password validation
        if user is not None:
            if user.username != username:
                return rt("login.html", error = "Invalid username!!")
            elif user.password != password:
                return rt("login.html", error = "Invalid password!!")
        else:
            return rt("login.html", error = "User not found!!")
        

        
        return rt("home.html") #redirect to dashboard later


# route for signup

@app.route('/register' , methods = ['GET' , 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        print(fullname , email , username , password)

        user = User(fullname = fullname , email = email , username = username , password = password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    
    elif request.method == 'GET':
        return rt("register.html")


@app.route('/gpt' , methods = ['GET' , 'POST'])
def gpt():
    return rt("home2.html")