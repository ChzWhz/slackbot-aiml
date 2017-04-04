#!/usr/bin/python2.7
import json
import os
import subprocess
import time
import settings
import aimlHandler
from slackclient import SlackClient

# constants
at_bot = "<@" + settings.bot_id + ">"

# instantiate Slack & Twilio clients
slack_client = SlackClient(settings.slack_bot_token)

def handle_command(command, channel):
    response = aimlHandler.kernel.respond(command)
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and at_bot in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(at_bot)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Bot is activated!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
