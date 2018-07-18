#!usr/bin/env python3

import sqlite3
import os


connection = sqlite3.connect('byte_master.db', check_same_thread=False)
cursor     = connection.cursor()

#os.system('rm byte_master.db')

cursor.execute(
    """CREATE TABLE students(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name VARCHAR(32),
        last_name VARCHAR(32),
        slack_id VARCHAR(32),
        email VARCHAR(32),
        phone VARCHAR(16),
        github_id VARCHAR(32),
        cohort INTEGER,
        week INTEGER,
        length INTEGER,
        birth_date DATE,
        course VARCHAR(16),
        project_1 VARCHAR(32),
        doc_1 BOOL,
        project_2 VARCHAR(32),
        doc_2 BOOL,
        absences INTEGER
    );"""
)


cursor.execute(
    """CREATE TABLE quizzes(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        prompt VARCHAR,
        github_link VARCHAR
    );"""
)


cursor.execute(
    """CREATE TABLE presentations(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_1 VARCHAR(32),
        topic_2 VARCHAR(32),
        topic_3 VARCHAR(32),
        topic_4 VARCHAR(32),
        topic_5 VARCHAR(32),
        topic_6 VARCHAR(32),
        topic_7 VARCHAR(32),
        topic_8 VARCHAR(32)
    );"""
)


cursor.execute(
    """CREATE TABLE cohorts(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR,
        start DATE,
        end DATE,
        week INTEGER,
        start_students INTEGER,
        end_students INTEGER,
        slack_channel VARCHAR
    );"""
)


connection.commit()
cursor.close()
connection.close()
