import os
import time
import re
import schedule
import random
import sys
from slackclient import SlackClient


# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

# Bytebot's user ID in Slack: value is assigned after the bot starts up
#starterbot_id = None

# constants
VERSION = 'Abernathy'
RTM_READ_DELAY = 3 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events, starter_id):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        with open('slack_events.txt', 'a+') as events_file:
            event_str = (str(event) + '\n')
            events_file.write(event_str)
        print(event)
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starter_id:
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

def handle_command(command, channel, starter_id, sending_user):
    """
        Executes bot command if the command is known
    """
    print('Command found!!')
    post=True
    username = 'ByteBot'
    emoji = ':byte:'
    
    reply_user = slack_client.api_call(
                "users.info",
                user=sending_user
                )['user']['profile']['real_name']
    print('\n', reply_user, '\n')

    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}* or *{}*.".format('hi', 'status')

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!

    if command.startswith('explain attendance'):
        username = 'attendancebot'
        emoji = ':slack:'
        slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text='Ok! I\'ll be taking attendance tomorrow, let me explain \
how that\'ll work....',
        username=username,
        icon_emoji=emoji)
        time.sleep(2)
        response = 'Tomorrow around 10:00 I\'ll post a message in \
your channel. All you have to do is respond with an emoji (any emoji \
will do) and I\'ll collect the responses a little bit later. If you \
have any other questions, ask Greg!'

    elif command.startswith('hello') or command.startswith('hi'):
        response = 'Hi!!'

    elif command.startswith("how are you"):
        response_list = ['Fine.', 'Bored', 'Waiting for a real command', 'Jaded', ':face_vomiting:']
        response = random.choice(response_list)

    elif command.startswith("status"):
        my_name = os.path.basename(sys.argv[0]).split('.')[0]
        process = os.getpid()
        username = str(my_name)
        emoji = ':slack:'
        response = "ByteBot Online.\nVersion: {}\nPID: {}\nSlack ID: {}".format(VERSION, process, starter_id)

    # Sends the response back to the channel
    
    elif command.startswith('analysis'):
        pass

    elif command.startswith('lookup Greg'):
        print(slack_client.api_call(
                "users.info",
                user='U8BE9UNHF'
                )['user']['real_name'])
        response = 'Looked Greg up (check your terminal)'

    elif command.startswith('help'):

        slide('U8BE9UNHF', reply_user)
        post=False

    if post==True:
        slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response,
        username=username,
        icon_emoji=emoji
    )

def slide(user_id, reply_user):
    """
        Sends Bytebot to DM a user
    """
    response = "{} needs your assistance".format(reply_user)
    slack_client.api_call(
        "chat.postMessage",
        channel=user_id,
        text=response,
        username='ByteBot',
        icon_emoji=':python:'
    )

