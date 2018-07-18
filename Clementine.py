import os
import time
from pprint import pprint
from slackclient import SlackClient

from attendance import *
from quizzes import *

# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

# Bytebot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM



if __name__ == "__main__":
    if slack_client.rtm_connect():
        print("ByteBot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        my_channel_list = get_channels()
        print(my_channel_list)
        morning_attendance = False
        afternoon_attendance = False
        #pprint(get_usr_info('U1K2NBXUG'))
        #prompt = obtain_quiz(1)
        #dispatch_quiz(prompt, 'U1K2NBXUG')
        #dispatch_quiz(prompt, 'U8BE9UNHF')
        
        while True:
            if morning_attendance == False and int(time.strftime('%H')) == 10:
                morning_attendance = True
                afternoon_attendance = False
                attendance_protocol('10:00', cohorts=my_channel_list)
                #slide_staff_dms('U1K2NBXUG')
                slide_staff_dms('U8BE9UNHF')
            elif afternoon_attendance == False and int(time.strftime('%H')) == 13:
                morning_attendance = False
                afternoon_attendance = True
                attendance_protocol('1:00', cohorts=my_channel_list)
                #slide_staff_dms('U1K2NBXUG')
                slide_staff_dms('U8BE9UNHF')
        time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
    