from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)

    content = db.Column('content', db.Text)
    type = db.Column('type', db.Integer)

class Option(db.Model):
    __tablename__ = "options"
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column('question_id', db.Integer, ForeignKey('questions.id'))
    option = db.Column('option', db.Text)
    value = db.Column('value', db.Integer)

class Answer(db.Model):
    __tablename__ = "answers"

    person_id = db.Column('person_id', db.Integer, ForeignKey('persons.id'), primary_key=True)
    question_id = db.Column('question_id', db.Integer, ForeignKey('questions.id'), primary_key=True)
    answer = db.Column('answer', db.Text)


class Person(db.Model):
    __tablename__ = "persons"

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column('full_name', db.Text)
    age = db.Column('age', db.Integer)
    city = db.Column('city', db.Text)
    gender = db.Column('gender', db.Text)
    native_languages = db.Column('native_languages', db.Text)