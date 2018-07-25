import os
import time
from pprint import pprint
from slackclient import SlackClient


# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

# Bytebot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 3 # 1 second delay between reading from RTM


def attendance_protocol(hour, cohorts):
    """
        Executes bot command if the command is known
    """

    sent_attendance = []
    date = time.strftime("%Y_%m_%d")
    for cohort in cohorts:
        channel, msg_time = post_attendance(channel=cohort[1], cohort_name=cohort[0])
        sent_attendance.append((channel, msg_time, cohort[0]))

    time.sleep(600)
    with open('attendance_{}.csv'.format(date), 'a+') as a_report:
        a_report.write('name,time,cohort,date\n')
        for attendance in sent_attendance:
            response_json = take_attendance(channel=attendance[0], ts=attendance[1])
            print(len(response_json))
            attendance_report = []
            for _ in range(len(response_json)):
                (attendance_report.append(response_json[_]["users"]))
            print(attendance_report)
            try:
                for user in attendance_report:
                    name = (slack_client.api_call(
                        "users.info",
                        user=user[0]
                        )['user']['real_name'])
                    print(name)
                    a_report.write('{},{},{},{}\n'.format(name, hour, attendance[2], date))
            except:
                print('No check-ins recorded')
    print('\nCSV Written!!\n')
    #acceptance = slide_staff_dms('U8BE9UNHF')


def post_attendance(channel, cohort_name):
    """
        Posts attendance message in given channel id
    """
    attendance_message = "{}, please check in with an emoji response below! \
    (Only one response each, please)".format(cohort_name)

    msg_ts = slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=attendance_message,
        icon_emoji=':byte:')["ts"],
    return(channel, msg_ts)

def take_attendance(channel, ts):
    """
        Parses attendance message for reactions
    """
    try:
        attendance = slack_client.api_call(
            "reactions.get",
            channel="{}".format(channel),
            timestamp="{}".format(ts)
        )["message"]["reactions"]
        return attendance
    except:
        print('No check-ins recorded so far')
        return []

def get_channels():
    """
        Obtains list of channels ByteBot has been added to on startup
    """
    my_channels = []
    channels = slack_client.api_call(
            "channels.list",
            exclude_archived='true',
            exclude_members='true'
        )["channels"]
    for channel in channels:
        if channel["is_member"]:
            my_channels.append((channel['name'], channel['id']))
    return my_channels

def slide_staff_dms(slack_id):
    """
        Slide's into Greg's DMs and asks him to sign off 
        on attendance (*debugging/alpha version only*)
    """

    user_name = slack_client.api_call(
                "users.info",
                user=slack_id
                )['user']['real_name']
    response = "Heyyy"
    slack_client.api_call(
        "chat.postMessage",
        channel=slack_id,
        text=response,
        attachments=[
        {
            "text": "Sign off below",
            "fallback": "You need to sign off for submission",
            "callback_id": "attendance_signoff",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "option",
                    "text": "Yes",
                    "type": "button",
                    "value": "yes"
                },
                {
                    "name": "option",
                    "text": "No",
                    "type": "button",
                    "value": "no"
                }
            ]
        }
    ],
        username='ByteBot',
        icon_emoji=':byte:')

def get_usr_info(user_id):
    response = slack_client.api_call(
                "users.info",
                user=user_id
                )
    return response
