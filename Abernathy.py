import os
import sys
import time
import schedule
import threading
import re
import random
from pprint import pprint
from slackclient import SlackClient

from attendance import *
from quizzes import *
from interactions import *

# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

# Bytebot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None
# constants
VERSION = 'Abernathy'
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
DELAY = 3 # 1 second delay between reading from RTM

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

def job_1():
    print('job1')
    attendance_protocol('10:00', cohorts=my_channel_list)

def job_2():
    attendance_protocol('1:00', cohorts=my_channel_list)

def job_3():
    quiz_protocol([('testchannel', 'CBLUAP3J5')])

def job_4():
    pass

if __name__ == "__main__":
    if slack_client.rtm_connect():
        print("ByteBot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        print(starterbot_id)
        my_channel_list = get_channels()
        print(my_channel_list)
        #pprint(get_usr_info('U1K2NBXUG'))
        #prompt = obtain_quiz(1)
        #dispatch_quiz(prompt, 'U1K2NBXUG')
        #dispatch_quiz(prompt, 'U8BE9UNHF')

        schedule.every().monday.at("10:00").do(run_threaded, job_3)
        schedule.every().monday.at("10:00").do(run_threaded, job_1)
        schedule.every().tuesday.at("10:00").do(run_threaded, job_1)
        schedule.every().wednesday.at("10:00").do(run_threaded, job_1)
        schedule.every().thursday.at("10:00").do(run_threaded, job_1)
        schedule.every().friday.at("10:00").do(run_threaded, job_1)

        schedule.every().monday.at("13:00").do(run_threaded, job_2)
        schedule.every().tuesday.at("13:00").do(run_threaded, job_2)
        schedule.every().wednesday.at("13:00").do(run_threaded, job_2)
        schedule.every().thursday.at("13:00").do(run_threaded, job_2)
        schedule.every().friday.at("13:00").do(run_threaded, job_2)
        schedule.every().friday.at("21:00").do(run_threaded, job_4) 

        while 1:
            command, channel, user = parse_bot_commands(slack_client.rtm_read(), starterbot_id)
            if command:
                print('command!!!!!')
                run_threaded(handle_command(command, channel, starterbot_id, user))
            schedule.run_pending()
            #slide_staff_dms('U8BE9UNHF')
            #slide_staff_dms('U1K2NBXUG')
            time.sleep(DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
    