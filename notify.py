from slackclient import SlackClient
def sendMessage(message):
    token = "ixoxb-517333598005-586257567925-dpppckSdlQBUb9MWFLx83FjU"      # found at https://api.slack.com/web#authentication
    sc = SlackClient(token)
    sc.api_call(
            "chat.postMessage", channel="#general", text=message,
            username='sherlock', icon_emoji=':robot_face:'
    )
