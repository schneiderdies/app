from flask import Flask, render_template, redirect, url_for, request
from sqlalchemy import func

import models
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///form.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)


def addQuestion(content, type, options):
    q = Question(content=content, type=type)
    db.session.add(q)
    db.session.commit()
    db.session.refresh(q)
    if type == 2:
        i = 0
        for option in options:
            i += 1
            db.session.add(Option(question_id=q.id, option=option, value=len(options) - i))
    db.session.commit()


@app.route('/')
def index():
    db.create_all()
    db.session.commit()
    # models.Question.query.delete()
    # db.session.commit()
    addQuestion('Любите ли вы читать?', 2, ['Да', 'Больше да, чем нет', 'Больше нет, чем да', 'Нет'])
    addQuestion('Какая ваша любимая книга?', 1, [])
    addQuestion('Сколько времени в день вы в среднем тратите на чтение книг?', 2, ['10-20 минут', '20-30 минут', '30-40 минут', '40-50 минут', 'Час и больше'])
    addQuestion('Что мешает вам читать больше?', 2, ['Нет времени', 'Нет желания', 'Другое'])
    addQuestion('Кто ваш любимый автор?', 1, [])
    addQuestion('Какую книгу вы бы посоветовали прочитать всем?', 1, [])
    addQuestion('Прислушиваетесь ли вы к чьим-то рекомендациям при выборе книги?', 2, ['Да', 'Да, но не всегда', 'Чаще нет', 'Нет'])
    addQuestion('Чьё мнение для вас наиболее авторитетно при выборе книги?', 2, ['Семьи', 'Близких друзей', 'Знакомых', 'Другое'])
    addQuestion('Как вы относитесь к классической литературе?', 2, ['Очень хорошо', 'Хорошо', 'Удовлетворительно', 'Плохо'])
    addQuestion('Как вы относитесь к современной литературе?', 2, ['Очень хорошо', 'Хорошо', 'Удовлетворительно', 'Плохо'])
    return render_template("index.html")


@app.route('/form')
def form():
    questions = Question.query.all()
    options = Option.query.all()
    return render_template(
        'questions.html',
        questions=questions,
        options=options
    )


@app.route('/process', methods=['get'])
def answer_process():
    if not request.args:
        return redirect(url_for('question_page'))
    user = Person(
        full_name=request.args.get('full_name'),
        age=request.args.get('age'),
        city=request.args.get('city'),
        gender=request.args.get('gender'),
        native_languages=request.args.get('languages')
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    questions = Question.query.all()
    for question in questions:
        db.session.add(
            Answer(person_id=user.id, question_id=question.id, answer=request.args.get('q' + str(question.id))))
    db.session.commit()
    return redirect(url_for('results'))


@app.route('/results')
def results():
    all_info = {}
    age_stats = db.session.query(
        func.avg(Person.age),
        func.min(Person.age),
        func.max(Person.age)
    ).one()
    all_info['age_mean'] = age_stats[0]
    all_info['age_min'] = age_stats[1]
    all_info['age_max'] = age_stats[2]
    all_info['total_count'] = Person.query.count()
    return render_template('results.html', all_info=all_info)


if __name__ == '__main__':
    app.run(debug=False)