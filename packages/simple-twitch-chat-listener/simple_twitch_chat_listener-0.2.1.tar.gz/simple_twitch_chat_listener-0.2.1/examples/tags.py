from simple_twitch_chat_listener import TwitchChatListener

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip("#")
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def print_colored(text, hex_color):
    rgb_color = hex_to_rgb(hex_color)
    colored_text = f"\033[38;2;{rgb_color[0]};{rgb_color[1]};{rgb_color[2]}m{text}\033[0m"
    return colored_text

def chat_handler(username, message, tags = {}) -> None:
    if len(tags) == 0:
        print(f"{username}: {message}")
    else:
        if tags["color"] != "":
            username = print_colored(username, tags["color"])
        print(f"{username}: {message}")


tc = TwitchChatListener("goldenbeaster", twitch_irc_capability_tags=True)
tc.set_client_message_handler(chat_handler)
tc.start()

import time
time.sleep(30)

tc.stop()
