#importing flask things
from flask import render_template as rt , request , redirect , url_for , session , flash

#app import from app.py
from app import app

#model import from model.py
from models.model import *


#this will be the homepage of the website. It is not finised yet.
@app.route('/' , methods = ['GET' , 'POST'])
def home():
    print("route accessed")
    return rt("home.html")


# route for signup

@app.route('/register' , methods = ['GET' , 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        print(fullname , email , username , password)

        #exception handling:
        #ex-1 -> used username

        user1 = User.query.filter_by(username = username).first()
        if user1 is not None:
            return rt("register.html" , error = "This username is already taken. Please choose a new username")
    

        user = User(fullname = fullname , email = email , username = username , password = password)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    elif request.method == 'GET':
        return rt("register.html")



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
        if user is not None:  #user exists but checking if smth is wrong.
            if user.username != username:
                return rt("login.html", error = "Invalid username!!")
            elif user.password != password:
                return rt("login.html", error = "Invalid password!!")
        else:
            return rt("login.html", error = "User not found!!")
        
        #handles admin login. 
        if user.username == 'Admin':
            session['username'] = user.username
            return redirect(url_for('admin_dash')) 

        #handles user login.
        session['username'] = user.username
        return redirect(url_for('dashboard')) #redirect to dashboard later




#user_dashboard routes
@app.route('/dashboard/<string:username>' , methods = ['GET' , 'POST'])
def dashboard(username):      
    if 'username' in session:
        user = User.query.filter_by(username = username).first()
        return rt("dashboard.html" , user = user)    
    else:
        return redirect(url_for('login'))
    

@app.route('/scores' , methods = ['GET' , 'POST'])
def scores(username):
    if 'username' in session:
        user = User.query.filter_by(username = username).first()
        return rt("scores.html" , user = user)
    else:
        return redirect(url_for('login'))







#Admin_Dashboard Routes
@app.route('/admin_dash' , methods = ['GET' , 'POST'])
def admin_dash():
    if 'username' in session:
        user = User.query.filter_by(username = session['username']).first()        
        quizzes = Quiz.query.join(Chapter).all()
        return rt("admin_dash.html" , user = user , quizzes = quizzes)
    else:
        return redirect(url_for('login'))

#create quiz route
@app.route('/create_quiz/<string:username>' , methods = ['GET' , 'POST'])
def create_quiz(username):
    if username not in session:
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        return rt("create_quiz.html")
    elif request.method =='POST':
        date_of_quiz = request.form['date_of_quiz']
        duration = request.form['duration']
        chapterID = request.form['chapterID']

        quiz = Quiz(date_of_quiz = date_of_quiz , duration = duration , remarks = remarks , chapterID = chapterID)
        db.session.add(quiz)
        db.session.commit()

        return redirect(url_for('admin_dash'))




@app.route('/gpt' , methods = ['GET' , 'POST'])
def gpt():
    return rt("home2.html")