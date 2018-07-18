#!usr/bin/env python3

import sqlite3
import pandas as pd
from flask import Flask, render_template, request, url_for, redirect

import model

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        return "logged in!!!!!"

@app.route('/lookup/', methods=['GET', 'POST'])
def lookup():
    if request.method == 'GET':
        return render_template('lookup.html')
    else:
        try:
            query = request.form['studentsearch']
            query = query.split()
            first_name = query[0].title()
            last_name = query[1].title() if len(query) > 1 else None
            students = model.lookup_student(first_name, last_name)
            return render_template('lookup_students.html', students=students)
        except:
            query = request.form['cohortsearch'].lower()
            cohort, students = model.lookup_cohort(query)
            return render_template('lookup_cohort.html', cohort= cohort, students=students)

@app.route('/lookup_students/', methods=['GET', 'POST'])
def lookup_student():
    if request.method == 'GET':
        students = model.lookup_student('Gregory')
#        return 'Lookup'
        return render_template('lookup_students.html', students=students)

@app.route('/lookup_cohort/', methods=['GET', 'POST'])
def lookup_cohort():
    if request.method == 'GET':
        cohort, students = model.lookup_cohort('zerg')
#        return 'Lookup'
        return render_template('lookup_cohort.html', cohort=cohort, students=students)

@app.route('/edit/', methods=['GET', 'POST'])
def edit_student():
    if request.method == 'GET':
        return 'Edit students, cohorts, presentations, quizzes'
#        return render_template('lookup.html')

@app.route('/add_student/', methods=['GET', 'POST'])
def add_student():
    if request.method == 'GET':
        return render_template('add_student.html')
    else:
        first_name = (request.form['first_name']).title()
        last_name = (request.form['last_name']).title()
        slack_id = request.form['slack_id']
        email = request.form['email']
        phone_num = request.form['phone_num']
        github_id = request.form['github_id']
        cohort = request.form['cohort']
        week = request.form['week']
        length = request.form['length']
        birthday = request.form['birthday']
        course_type = request.form['course_type']
        project_1 = request.form['project_1']
        design_1 = 1 if (request.form['design_1'].lower()) == 'True' else 0
        project_2 = request.form['project_2']
        design_2 = 1 if (request.form['design_2'].lower()) == 'True' else 0
        print(first_name, last_name, slack_id, email, phone_num, github_id, cohort, 
        week, length, birthday, course_type, project_1, design_1, project_2, design_2)
        success = model.add_student(first_name, last_name, slack_id, email, phone_num, 
        github_id, cohort, week, length, birthday, course_type, project_1, design_1, 
        project_2, design_2, absences =0)
        if success:
            return render_template('home.html', message='Student added!')
        else:
            return render_template('add_student.html', 
            message = 'Error adding student, please try again')

@app.route('/add_cohort/', methods=['GET', 'POST'])
def add_cohort():
    if request.method == 'GET':
        return render_template('add_cohort.html')
    else:
        cohort_name = (request.form['cohort_name']).title()
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        week = request.form['week']
        start_students = request.form['start_students']
        end_students = request.form['end_students']
        slack_channel = request.form['slack_channel']
        success = model.add_cohort(cohort_name, start_date, end_date,
                                start_students, end_students, slack_channel)
        print(cohort_name, start_date, end_date, start_students, end_students, slack_channel)
        if success:
            return render_template('home.html', message='Cohort added!')
        else:
            return render_template('add_cohort.html', 
                        message = 'Error adding cohort, please try again')

@app.route('/add_quiz/', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'GET':
        return render_template('add_quiz.html')
    else:
        week = request.form['week']
        prompt = request.form['prompt']
        github_link = request.form['github_link']
        success = model.add_quiz(prompt, github_link)
        print(week, prompt, github_link)
        if success:
            return render_template('home.html', message='Quiz added!')
        else:
            return render_template('add_quiz.html', 
                        message = 'Error adding cohort, please try again')        

@app.route('/add_topics/', methods=['GET', 'POST'])
def add_topics():
    if request.method == 'GET':
        return render_template('add_presentation.html')
    else:
        week = request.form['week']
        topic_1 = request.form['topic_1']
        topic_2 = request.form['topic_2']
        topic_3 = request.form['topic_3']
        topic_4 = request.form['topic_4']
        topic_5 = request.form['topic_5']
        topic_6 = request.form['topic_6']
        topic_7 = request.form['topic_7']
        topic_8 = request.form['topic_8']
        success = model.add_topics(topic_1, topic_2, topic_3, topic_4,
                                   topic_5, topic_6, topic_7, topic_8)
        print(week, topic_1, topic_2, topic_3, topic_4, 
                topic_5, topic_6, topic_7, topic_8)
        if success:
            return render_template('home.html', message='Topics added!')
        else:
            return render_template('add_presentations.html', 
                        message = 'Error adding new topics, please try again')        



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
