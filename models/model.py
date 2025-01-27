from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    userID = db.Column(db.Integer, primary_key=True , autoincrement=True)
    fullname = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    type = db.Column(db.String(15), nullable=False , default = 'public')
    


class Subject(db.Model):
    __tablename__ = 'subject'
    subjectID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subjectName = db.Column(db.String(80), unique=True, nullable=False)
    subjectDescription = db.Column(db.String(120))


class Chapter(db.Model):
    __tablename__ = 'chapter'
    chapterID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chapterName = db.Column(db.String(80), unique=True, nullable=False)
    chapterDescription = db.Column(db.String(120))
    subjectID = db.Column(db.Integer, db.ForeignKey('subject.subjectID'), nullable=False)
    


class Quiz(db.Model):
    __tablename__ = 'quiz'
    quizID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_of_quiz = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    remarks = db.Column(db.String(120))
    chapterID = db.Column(db.Integer, db.ForeignKey('chapter.chapterID'), nullable=False)


class Question(db.Model):
    __tablename__ = 'question'
    questionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(120), nullable=False)
    option1 = db.Column(db.String(120), nullable=False)
    option2 = db.Column(db.String(120), nullable=False)
    option3 = db.Column(db.String(120), nullable=False)
    option4 = db.Column(db.String(120), nullable=False)
    correct_option = db.Column(db.String(120), nullable=False)
    quizID = db.Column(db.Integer, db.ForeignKey('quiz.quizID'), nullable=False)


class Scores(db.Model):
    __tablename__ = 'scores'
    scoreID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    quizID = db.Column(db.Integer, db.ForeignKey('quiz.quizID'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    