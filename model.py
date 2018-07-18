#!usr/bin/env python3

import sqlite3
import pandas as pd

def lookup_student(first_name, last_name=None):
    connection = sqlite3.connect('byte_master.db', check_same_thread = False)
    cursor     = connection.cursor()
    first_name = str(first_name.title())
    try:
        last_name = str(last_name.title())
        cursor.execute("SELECT * FROM students WHERE first_name = '{}' AND last_name = '{}';".format(
                                                                                first_name, last_name))
        rows = pd.DataFrame(cursor.fetchall(), columns=['pk', 'first_name','last_name',
        'slack_id', 'email', 'phone_num', 'github_id', 'cohort', 'week', 'length',
        'birthday', 'course_type', 'project_1', 'doc_1', 'project_2', 'doc_2', 'absences'])
    except:
        cursor.execute("SELECT * FROM students WHERE first_name = '{}';".format(first_name))
        rows = pd.DataFrame(cursor.fetchall(), columns=['pk', 'first_name','last_name',
        'slack_id', 'email', 'phone_num', 'github_id', 'cohort', 'week', 'length',
        'birthday', 'course_type', 'project_1', 'doc_1', 'project_2', 'doc_2', 'absences'])
    rows.set_index('pk', inplace=True)
#    rows = rows.reset_index(drop = True, inplace = True)
    print(rows)
    rows = rows.to_html()
 #   print(rows)
    return rows

def lookup_cohort(name):
    cohort_name = str(name.lower())
    connection = sqlite3.connect('byte_master.db', check_same_thread = False)
    cursor     = connection.cursor()
    cursor.execute("SELECT * FROM cohorts WHERE name= '{}';".format(cohort_name))
    cohort = pd.DataFrame(cursor.fetchall(), columns=['pk', 'name','start',
    'end', 'week', 'start_students', 'end_students', 'slack_channel'])
    cohort_id = cohort['pk'][0]
    cursor.execute("SELECT * FROM students WHERE cohort = {};".format(cohort_id))
    students = pd.DataFrame(cursor.fetchall(), columns=['pk', 'first_name','last_name',
    'slack_id', 'email', 'phone_num', 'github_id', 'cohort', 'week', 'length',
    'birthday', 'course_type', 'project_1', 'doc_1', 'project_2', 'doc_2', 'absences'])
    cohort.set_index('pk', inplace=True)
    students.set_index('pk', inplace=True)
#    row = row.reset_index(drop = True, inplace = True)
    print(cohort)
    print('\n')
    print(students)
    cohort = cohort.to_html()
    students = students.to_html()
 #   print(rows)
    return cohort, students

def add_student(fn, ln, slack, email, phone, gh_id, cohort, week, length,
        birthday, course, proj1, doc1, proj2, doc2, absences):
    connection = sqlite3.connect('byte_master.db', check_same_thread = False)
    cursor     = connection.cursor()
    print(fn, ln, slack, email, phone, gh_id, cohort, week, length, birthday, 
            course, proj1, doc1, proj2, doc2, absences)
    sql_command = """INSERT INTO students(
        first_name,last_name,slack_id,email,phone,github_id,cohort,week,
        length,birth_date,course,project_1,doc_1,project_2,doc_2,absences
        ) VALUES(
        '{}','{}','{}','{}','{}','{}',{},{},{},'{}','{}','{}',{},
        '{}',{},{});""".format(fn, ln, slack, email, phone, gh_id, cohort,
        week, length, birthday, course, proj1, doc1, proj2, doc2, absences)
    print(sql_command)
    try:
        cursor.execute(sql_command)
        connection.commit()
        cursor.close()
        return True
    except:
        return False

def add_cohort(name,start,end,week,start_students,end_students,slack_channel):
    connection = sqlite3.connect('byte_master.db', check_same_thread = False)
    cursor     = connection.cursor()
    print(name,start,end,start_students,end_students,slack_channel)
    sql_command = """INSERT INTO cohorts(
        name,start,end,week,start_students,end_students,slack_channel
        ) VALUES(
        '{}','{}','{}',{},{},{},'{}');""".format(name,start,end,week,
                            start_students,end_students,slack_channel)
    print(sql_command)
    try:
        cursor.execute(sql_command)
        connection.commit()
        cursor.close()
        return True
    except:
        return False

def add_quiz(prompt,github_link):
    connection = sqlite3.connect('byte_master.db', check_same_thread = False)
    cursor     = connection.cursor()
    print(prompt,github_link)
    sql_command = """INSERT INTO quizzes(prompt,github_link) VALUES(
        '{}','{}');""".format(prompt,github_link)
    print(sql_command)
    try:
        cursor.execute(sql_command)
        connection.commit()
        cursor.close()
        return True
    except:
        return False

def add_topics(topic_1, topic_2, topic_3, topic_4, topic_5, topic_6, topic_7, topic_8):
    connection = sqlite3.connect('byte_master.db', check_same_thread = False)
    cursor     = connection.cursor()
    print(topic_1, topic_2, topic_3, topic_4, topic_5, topic_6, topic_7, topic_8)
    sql_command = """INSERT INTO presentations(topic_1, topic_2, topic_3,
    topic_4, topic_5, topic_6, topic_7, topic_8) VALUES(
        '{}','{}','{}','{}','{}','{}','{}','{}');""".format(topic_1,
        topic_2, topic_3, topic_4, topic_5, topic_6, topic_7, topic_8)
    print(sql_command)
    try:
        cursor.execute(sql_command)
        connection.commit()
        cursor.close()
        return True
    except:
        return False

