import simple_twitch_chat_listener
import time

CHANNEL_NAME = "goldenbeaster"

def my_message_handler(username, message):
    print(f"{username}: {message}")

def connect_to_channel(channel_name, message_handler):
    tc = simple_twitch_chat_listener.TwitchChatListener(channel_name)
    tc.set_client_message_handler(message_handler)
    tc.start()
    return tc

tc = connect_to_channel(CHANNEL_NAME, my_message_handler)

time.sleep(10)
# once you want to stop the service
tc.stop()
time.sleep(5)

# We currently recreate the object, because I am too scared to fix the new thread issue
tc = connect_to_channel(CHANNEL_NAME, my_message_handler)
time.sleep(10)

tc.stop()
