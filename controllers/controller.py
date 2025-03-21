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
        return redirect(url_for('User.dashboard')) #redirect to dashboard later






#Admin_Dashboard Routes
@app.route('/Admin/admin_dash' , methods = ['GET' , 'POST'])
def admin_dash():
    if 'username' in session:
        user = User.query.filter_by(username = session['username']).first()        
        quizzes = Quiz.query.join(Chapter).all()
        return rt("Admin/admin_dash.html" , user = user , quizzes = quizzes)
    else:
        return redirect(url_for('login'))



#Subject management routes
@app.route('/subjects' , methods = ['GET' , 'POST'])
def subjects():
    if ('username' in session) and (session['username'] == 'Admin'):
        subjects = Subject.query.all()
        return rt("Admin/Subject/subjects.html" , subjects = subjects)
    else:
        return redirect(url_for('login'))


#Chapter Management routes
@app.route('/chapters' , methods = ['GET' , 'POST'])
def chapters():
    if ('username' in session) and (session['username'] == 'Admin'):
        chapters = Chapter.query.all()
        subjects = Subject.query.all()
        return rt("Admin/chapters.html" , chapters = chapters , subjects = subjects)
    else:
        return redirect(url_for('login'))



#Add Subject route
@app.route('/add_subject' , methods = ['GET' , 'POST'])
def add_subject():
    if ('username' in session) and (session['username'] == 'Admin'):
        if request.method == 'GET':
            return rt("Admin/Subject/add_subject.html")
        elif request.method == 'POST':
            subjectName = request.form['sub_name']
            subjectDescription = request.form['sub_desc']
            subject = Subject(subjectName = subjectName , subjectDescription = subjectDescription)
            db.session.add(subject)
            db.session.commit()
            return redirect(url_for('subjects'))
    else:
        return redirect(url_for('login'))


#Edit Subject Route
@app.route('/edit_sub/<int:subjectID>' , methods = ['GET' , 'POST'])
def edit_sub(subjectID):
    if ('username' in session) and (session['username'] == 'Admin'):
        subject = Subject.query.filter_by(subjectID = subjectID).first()
        
        #error handling in case subject not found
        if not subject:
            return "Subject not found!", 404
    
        if request.method == 'GET':
            return rt("Admin/Subject/edit_sub.html" , subject = subject)
        
        elif request.method == 'POST':
            subject.subjectName = request.form['sub_name']
            subject.subjectDescription = request.form['sub_desc']
            
            db.session.commit()
            return redirect(url_for('subjects'))


#Delete Subject Route
@app.route('/del_sub/<int:subjectID>' , methods = ['POST'])
def del_sub(subjectID):
    if ('username' in session) and (session['username'] == 'Admin'):
        subject = Subject.query.filter_by(subjectID = subjectID).first()
        
        #error handling in case subject not found
        if not subject:
            return "Subject not found!", 404
        
        db.session.delete(subject)
        db.session.commit()
        return redirect(url_for('subjects'))

#after admin wrk


#create quiz route
@app.route('/create_quiz/<string:username>' , methods = ['GET' , 'POST'])
def create_quiz(username):
    if (username not in session) or (session['username'] != 'Admin'):
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        return rt("create_quiz.html" , username = username)
    elif request.method =='POST':
        date_of_quiz = request.form['date_of_quiz']
        duration = request.form['duration']
        chapterID = request.form['chapterID']

        quiz = Quiz(date_of_quiz = date_of_quiz , duration = duration , chapterID = chapterID)
        db.session.add(quiz)
        db.session.commit()

        return redirect(url_for('admin_dash'))


#route for quiz management
@app.route('/quiz_management/<string:username>' , methods = ['GET' , 'POST'])
def quiz_management(username):
    if username != 'Admin':
        return redirect(url_for('login'))

    if request.method == 'GET':
        quizzes = Quiz.query.all()
        subjects = Subject.query.all()
        chapters = Chapter.query.all()
        user = User.query.filter_by(username = username).first()
        return rt("quiz_management.html" , quizzes = quizzes , user=user , subjects = subjects , chapters = chapters)








#user_dashboard routes
@app.route('/User/dashboard/<string:username>' , methods = ['GET' , 'POST'])
def dashboard(username):      
    if 'username' in session:
        user = User.query.filter_by(username = username).first()
        return rt("User/dashboard.html" , user = user)    
    else:
        return redirect(url_for('login'))
    

@app.route('/User/scores' , methods = ['GET' , 'POST'])
def scores(username):
    if 'username' in session:
        user = User.query.filter_by(username = username).first()
        return rt("User/scores.html" , user = user)
    else:
        return redirect(url_for('login'))








@app.route('/gpt' , methods = ['GET' , 'POST'])
def gpt():
    return rt("home2.html")