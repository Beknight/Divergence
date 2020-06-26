from slack import WebClient

def sendMessage(message):
    token = ""      # found at https://api.slack.com/web#authentication
    sc = WebClient(token)
    sc.chat_postMessage(
            channel="#general", text=message,
            username='sherlock', icon_emoji=':robot_face:'
    )
