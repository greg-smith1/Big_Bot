import sqlite3
import os
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def get_slack_ids(week):
    connection = sqlite3.connect('byte_master.db', check_same_thread = False)
    cursor     = connection.cursor()
    cursor.execute("SELECT FROM quizzes WHERE pk= '{}';".format(week))
    ids = cursor.fetchall()
    print(ids)
    return ids

def obtain_quiz(week):
    connection = sqlite3.connect('byte_master.db', check_same_thread = False)
    cursor     = connection.cursor()
    cursor.execute("SELECT * FROM quizzes WHERE pk= '{}';".format(week))
    quiz = cursor.fetchone()[1]
    print(quiz)
    return quiz

def dispatch_quiz(prompt, slack_id):
    slack_client.api_call(
        "chat.postMessage",
        channel=slack_id,
        text=prompt,
        username='ByteBot',
        icon_emoji=':python:'
    )
