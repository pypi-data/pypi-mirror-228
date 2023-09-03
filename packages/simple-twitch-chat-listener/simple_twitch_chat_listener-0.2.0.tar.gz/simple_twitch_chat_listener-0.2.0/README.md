# simple-twitch-chat-listener

Seeing the pure lack of twitch chat bots that are only meant for listening in and not requiring oauth tokens I decided to make my own.

This package is only meant for **Twitch** chat and is only capable of **receiving** messages, **not sending**

Pros:

- Does not require a oauth token
- Extremely simple setup
- Chat listener runs on a separate thread

Cons:

- Not much experience with edge case error handling

## Installation

```sh
pip install -U simple-twitch-chat-listener
```

## Example usage

```python
from simple_twitch_chat_listener import TwitchChatListener

def my_message_handler(username, message):
    print(f"{username}: {message}")

tc = TwitchChatListener("goldenbeaster")
tc.set_client_message_handler(my_message_handler)
tc.start()

# Place your code here
import time
time.sleep(10)
# endof place your code here

# once you want to stop the service
tc.stop()
```

Other examples can be found [here](./examples/)

## Stuff that still needs to be done

actual RECONNECT handling

network connectivity testing
