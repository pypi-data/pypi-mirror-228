import simple_twitch_chat_listener

def my_message_handler(username, message):
    print(f"{username}: {message}")

tc = simple_twitch_chat_listener.TwitchChatListener("goldenbeaster")
tc.set_client_message_handler(my_message_handler)
tc.start()

# Place your code here
import time
time.sleep(10)

# once you want to stop the service
tc.stop()
