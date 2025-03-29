#importing flask things
from flask import render_template as rt , request , redirect , url_for , session , flash

#app import from app.py
from app import app

#model import from model.py
from models.model import *

#random imports
from datetime import datetime
from sqlalchemy import func


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
        return redirect(url_for('dashboard' , username=session['username'])) #redirect to dashboard later username is stored in session


#route for logout
@app.route('/logout' , methods = ['GET' , 'POST'])
def logout():
    session.pop('username' , None)
    return redirect(url_for('login'))



#Admin_Dashboard Routes
@app.route('/Admin/admin_dash' , methods = ['GET' , 'POST'])
def admin_dash():
    if 'username' in session:
        user = User.query.filter_by(username = session['username']).first()   
        today = datetime.now().date()     
        quizzes = Quiz.query.join(Chapter).filter(Quiz.date_of_quiz >= today).all()
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
    else:
        return redirect(url_for('login'))


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
    else:
        return redirect(url_for('login'))



#Chapter Management routes
@app.route('/chapters' , methods = ['GET' , 'POST'])
def chapters():
    if ('username' in session) and (session['username'] == 'Admin'):
        chapters = Chapter.query.all()
        subjects = Subject.query.all()
        return rt("Admin/Chapter/chapters.html" , chapters = chapters , subjects = subjects)
    else:
        return redirect(url_for('login'))



#add Chapter route
@app.route('/add_chapter' , methods = ['GET' , 'POST'])
def add_chapter():
    if ('username' in session) and (session['username'] == 'Admin'):
        if request.method == 'GET':
            
            return rt("Admin/Chapter/add_chapter.html" , subjects = subjects)
        elif request.method == 'POST':
            chapterName = request.form['chp_name']
            chapterDescription = request.form['chp_desc']
            subjectID = request.form['sub_id']
            chapter = Chapter(chapterName = chapterName , chapterDescription = chapterDescription , subjectID = subjectID)
            db.session.add(chapter)
            db.session.commit()
            return redirect(url_for('chapters'))
    else:
        return redirect(url_for('login'))



#edit Chapter route
@app.route('/edit_chapter/<int:chapterID>' , methods = ['GET' , 'POST'])
def edit_chapter(chapterID):
    if ('username' in session) and (session['username'] == 'Admin'):
        chapter = Chapter.query.filter_by(chapterID = chapterID).first()
        
        #error handling in case chapter not found
        if not chapter:
            return "Chapter not found!", 404
    
        if request.method == 'GET':            
            return rt("Admin/Chapter/edit_chapter.html" , chapter = chapter)
        
        elif request.method == 'POST':
            chapter.chapterName = request.form['chp_name']
            chapter.chapterDescription = request.form['chp_desc']
                                    
            db.session.commit()
            return redirect(url_for('chapters'))
    else:
        return redirect(url_for('login'))


#delete chapter route
@app.route('/del_chapter/<int:chapterID>' , methods = ['POST'])
def del_chapter(chapterID):
    if ('username' in session) and (session['username'] == 'Admin'):
        chapter = Chapter.query.filter_by(chapterID = chapterID).first()
        
        #error handling in case chapter not found
        if not chapter:
            return "Chapter not found!", 404
        
        db.session.delete(chapter)
        db.session.commit()
        return redirect(url_for('chapters'))
    else:
        return redirect(url_for('login'))



#quiz management routes
@app.route('/quiz' , methods = ['GET' , 'POST'])
def quiz():
    if ('username' not in session) or (session['username'] != 'Admin'):
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        quizzes = Quiz.query.all()
        subjects = Subject.query.all()
        chapters = Chapter.query.all()
        
        return rt("Admin/Quiz/quiz.html", quizzes = quizzes , subjects = subjects , chapters = chapters)
    

#create quiz route   
@app.route('/create_quiz' , methods = ['GET' , 'POST'])
def create_quiz():
    if ('username' not in session) or (session['username'] != 'Admin'):
        return redirect(url_for('login'))       

    if request.method == 'GET':
        return rt("Admin/Quiz/create_quiz.html")
          
    elif request.method =='POST':          
        name = request.form['name']
        date_of_quiz = request.form['date_of_quiz']        
        formatted_date = datetime.strptime(date_of_quiz, '%Y-%m-%d').date()  # Convert to date format
        duration = request.form['duration']
        chapterID = request.form['chapterID']
        

        quiz = Quiz(quizName=name , date_of_quiz = formatted_date , duration = duration , chapterID = chapterID)
        db.session.add(quiz)
        db.session.commit()
          
        print("Redirecting to:", url_for('quiz'))
        return redirect(url_for('quiz'))



#route for editing quiz
@app.route('/edit_quiz/<int:quizID>' , methods = ['GET' , 'POST'])
def edit_quiz(quizID):
    if ('username' not in session) or (session['username'] != 'Admin'):
        return redirect(url_for('login'))
    
    quiz = Quiz.query.filter_by(quizID = quizID).first()
    if not quiz:
        return "Quiz not found!", 404
    
    if request.method == 'GET':
        return rt("Admin/Quiz/edit_quiz.html" , quiz = quiz)
    
    elif request.method == 'POST':
        date_of_quiz = request.form['date_of_quiz']
        formatted_date = datetime.strptime(date_of_quiz, '%Y-%m-%d').date()  # Convert to date format
        quiz.date_of_quiz = formatted_date
        quiz.duration = request.form['duration']
        quiz.quizName = request.form['name']
        
        db.session.commit()
        return redirect(url_for('quiz'))


        

#route for viewing quiz (edit and add questions here)
@app.route('/view_quiz' , methods = ['GET' , 'POST'])
def view_quiz():
    if ('username' not in session) or (session['username'] != 'Admin'):
        return redirect(url_for('login'))
    
    quizzes = Quiz.query.all()    
    
    if request.method == 'GET':
        return rt("Admin/Quiz/view_quiz.html" , quizzes = quizzes)



#delete quiz route
@app.route('/del_quiz/<int:quizID>' , methods = ['POST'])
def del_quiz(quizID):
    if ('username' in session) and (session['username'] == 'Admin'):
        quiz = Quiz.query.filter_by(quizID = quizID).first()
        
        #error handling in case chapter not found
        if not quiz:
            return "Quiz not found!", 404
        
        db.session.delete(quiz)
        db.session.commit()
        return redirect(url_for('quiz'))
    else:
        return redirect(url_for('login'))



#add question route
@app.route('/add_question/<int:quizID>' , methods = ['GET' , 'POST'])
def add_question(quizID):
    if ('username' not in session) or (session['username'] != 'Admin'):
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        return rt("Admin/Question/add_question.html" , quizID = quizID)
    elif request.method == 'POST':
        statement = request.form['question']
        A = request.form['A']
        B = request.form['B']
        C = request.form['C']
        D = request.form['D']
        answer = request.form['answer']        
        
        question = Question(question = statement , A=A , B = B , C = C , D = D , answer = answer , quizID = quizID)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('view_quiz'))


#route for editing question
@app.route('/edit_question/<int:questionID>' , methods = ['GET' , 'POST'])
def edit_question(questionID):
    if ('username' not in session) or (session['username'] != 'Admin'):
        return redirect(url_for('login'))
    
    question = Question.query.filter_by(questionID = questionID).first()
    if not question:
        return "Quiz not found!", 404
    
    if request.method == 'GET':
        return rt("Admin/Question/edit_question.html" , question = question)
    
    elif request.method == 'POST':
        question.question = request.form['question']
        question.A = request.form['A']
        question.B = request.form['B']
        question.C = request.form['C']
        question.D = request.form['D']
        question.answer = request.form['answer']
        
        db.session.commit()
        return redirect(url_for('view_quiz'))


#route for deleting question
@app.route('/del_question/<int:questionID>' , methods = ['POST'])
def del_question(questionID):
    if ('username' in session) and (session['username'] == 'Admin'):
        question = Question.query.filter_by(questionID = questionID).first()
        
        #error handling in case chapter not found
        if not question:
            return "Question not found!", 404
        
        db.session.delete(question)
        db.session.commit()
        return redirect(url_for('view_quiz'))
    else:
        return redirect(url_for('login'))


#route for Users in admin dashboard
@app.route('/users' , methods = ['GET' , 'POST'])
def users():
    if ('username' not in session) or (session['username'] != 'Admin'):
        return redirect(url_for('login'))
    
    users = User.query.filter_by(type='public').all()
    return rt("Admin/User/users.html" , users = users)


#route for deleting user account
@app.route('/del_user/<int:userID>' , methods = ['POST'])
def del_user(userID):
    if ('username' in session) and (session['username'] == 'Admin'):
        user = User.query.filter_by(userID = userID).first()
        
        #error handling in case chapter not found
        if not user:
            return "User not found!", 404
        
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('users'))
    else:
        return redirect(url_for('login'))



#user stuff starts here


#user dashboard route
@app.route('/dashboard/<string:username>' , methods = ['GET' , 'POST'])
def dashboard(username):      
    if 'username' not in session:        
        return redirect(url_for('login'))

    user = User.query.filter_by(username = username).first()
    today = datetime.now().date()
   
    upcoming_quizzes = Quiz.query.filter(func.date(Quiz.date_of_quiz) >= today).all()      
    ongoing_quizzes = Quiz.query.filter(func.date(Quiz.date_of_quiz) == today).all()
    past_quizzes = Quiz.query.filter(func.date(Quiz.date_of_quiz) < today).all()

    return rt("User/dashboard.html" , user = user , upcoming_quizzes = upcoming_quizzes , ongoing_quizzes = ongoing_quizzes , past_quizzes = past_quizzes)    
    


#route for viewing quiz
@app.route('/dashboard/<string:username>/quiz_details/<int:quizID>' , methods = ['GET' , 'POST'])
def quiz_details(username , quizID):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    
    quiz = Quiz.query.filter_by(quizID = quizID).first()
    
    return rt("User/quiz_details.html" , quiz = quiz)




#route for attempting quiz
@app.route('/dashboard/<string:username>/attempt_quiz/<int:quizID>' , methods = ['GET' , 'POST'])
def attempt_quiz(username , quizID):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user = User.query.filter_by(username = username).first()
    quiz = Quiz.query.filter_by(quizID = quizID).first()
    questions = Question.query.filter_by(quizID=quizID).all()
    #access questions thru quiz.questions
    if quiz is None:
        return "Quiz not found!", 404
    
    #handles if quiz is already attempted by the user.
    if Scores.query.filter_by(quizID = quizID , userID = user.userID).first():
        return "You have already attempted this quiz!", 404

    #handles if quiz is not active yet.
    if func.date(quiz.date_of_quiz) != datetime.now().date():
        return "This quiz cannot be attempted today!", 404
    

    if request.method == 'POST':
        #handle quiz submission here
        #get answers from form and save to database
        #calculate score and save to database
        
        score = 0
        total_questions = len(questions) #for total score. each questions holds 1 mark.

        for question in questions:
            user_answer = request.form.get(f'question_{question.questionID}') #used .get cuz if its empty it will cause error aka retun NONE.
            if user_answer and user_answer == question.answer: #check if the answer exists and is correct
                score += 1
        
        #save the score in the db
        user = User.query.filter_by(username = username).first()
        user_score = Scores(userID = user.userID , quizID = quizID , score = score)

        db.session.add(user_score)
        db.session.commit()

        return redirect(url_for('Score' , username = username , quizID = quizID)) #redirect to result page
        
    
    return rt("User/attempt_quiz.html" , quiz = quiz )




#route for viewing result
@app.route('/dashboard/<string:username>/result' , methods = ['GET' , 'POST'])
def result(username):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user = User.query.filter_by(username = username).first()
    scores = Scores.query.filter_by(userID = user.userID).all()
    
    
    return rt("User/result.html" , user = user , scores = scores) #will access quiz using backref part.






















#this one later

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