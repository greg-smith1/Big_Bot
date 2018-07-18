import os
import time
import re
import schedule
import random
from slackclient import SlackClient


# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

# Bytebot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 3 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If it's not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"], event["user"]
    return None, None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel, sending_user):
    """
        Executes bot command if the command is known
    """
    post=True
    reply_user = slack_client.api_call(
                "users.info",
                user=sending_user
                )['user']['real_name']

    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"

    elif command.startswith('hello') or command.startswith('hi'):
        response = 'Hi {}!!'.format(reply_user)

    elif command.startswith("how are you"):
        response_list = ['Fine.', 'Bored', 'Waiting for a real command, {}'.format(reply_user), 'Jaded', ':face_vomiting:']
        response = random.choice(response_list)

    elif command.startswith("say hi"):
        response = "Hi {}. But shouldn't you get me logging attendance?".format(reply_user)

    # Sends the response back to the channel

    elif command.startswith('post attendance'):
        msg_time = post_attendance(channel=channel, cohort_name='test_channel')
        time.sleep(15)
        response_json = take_attendance(channel=channel, ts=msg_time)
        print(len(response_json))
        attendance_report = []
        for _ in range(len(response_json)):
            (attendance_report.append(response_json[_]["users"]))
        response = 'Attendance reported!'
        print(attendance_report)
        with open('attendance.csv', 'w+') as a_report:
            a_report.write('name,time\n')
            for user in attendance_report:
                name = (slack_client.api_call(
                    "users.info",
                    user=user[0]
                    )['user']['real_name'])
                print(name)
                a_report.write('{},10:00\n'.format(name))
        print('\nCSV Written, Greg!!\n')
    
    elif command.startswith('lookup Greg'):
        print(slack_client.api_call(
                "users.info",
                user='U8BE9UNHF'
                )['user']['real_name'])
        response = 'Looked Greg up (check your terminal)'

    elif command.startswith('get Greg'):
        slide('U8BE9UNHF')
        post=False

    if post==True:
        slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response,
        username='ByteBot',
        icon_emoji=':python:'
    )

def post_attendance(channel, cohort_name):
    """
        Posts attendance message in given channel id
    """
    attendance_message = "{}, please check in with an emoji response below! \
    (Only one response each, please)".format(cohort_name)

    msg_ts = slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=attendance_message)["ts"]
    return(msg_ts)

def take_attendance(channel, ts):
    """
        Parses attendance message for reactions
    """
    attendance = slack_client.api_call(
        "reactions.get",
        channel="{}".format(channel),
        timestamp="{}".format(ts)
    )["message"]["reactions"]
    return attendance

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
            my_channels.append([channel['name'], channel['id']])
    return my_channels

def slide(user_id):
    """
        Sends Bytebot to DM a user
    """
    user_name = slack_client.api_call(
                "users.info",
                user=user_id
                )['user']['real_name']
    response = "Heyy"
    slack_client.api_call(
        "chat.postMessage",
        channel=user_id,
        text=response,
        username='ByteBot',
        icon_emoji=':python:'
    )

def attendance_protocol(hour, cohorts):
    pass

if __name__ == "__main__":
    if slack_client.rtm_connect():
        print("ByteBot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        my_channel_list = get_channels()
        while True:
            command, channel, sending_user = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel, sending_user)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")


"""
    morning_attendance = False
    afternoon_attendance = False
    if int(time.strftime(%H)) == 11:
        for channel in my_channel_list:
            post_attendance
"""