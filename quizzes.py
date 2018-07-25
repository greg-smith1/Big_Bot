import sqlite3
import os
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def get_week(slack_id):
    connection = sqlite3.connect('byte_master.db', check_same_thread = False)
    cursor     = connection.cursor()
    cursor.execute("SELECT week FROM cohorts WHERE slack_id= '{}';".format(slack_id))
    ids = cursor.fetchall()
    print(ids)
    return ids

def obtain_quiz(week):
    connection = sqlite3.connect('byte_master.db', check_same_thread = False)
    cursor     = connection.cursor()
    cursor.execute("SELECT * FROM quizzes WHERE week= '{}';".format(week))
    quiz = cursor.fetchone()[1]
    print(quiz)
    return quiz

def dispatch_quiz(prompt, slack_id):
    slack_client.api_call(
        "chat.postMessage",
        channel=slack_id,
        text=prompt,
        username='QuizBot',
        icon_emoji=':byte:'
    )

def quiz_protocol(cohorts):
    for cohort in cohorts:
        week = get_week(cohort[1])
        quiz = obtain_quiz(week)
        dispatch_quiz(quiz, cohort[1])

def update_week(table):
    connection = sqlite3.connect('byte_master.db', check_same_thread = False)
    cursor     = connection.cursor()
    cursor.execute("UPDATE {} SET week = week + 1;".format(table))
    connection.commit()
    cursor.close()
