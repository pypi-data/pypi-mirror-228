import asyncio
import websockets
import re
import threading
import time
import random
from typing import Callable, Union

class TwitchChatListener:
    def __init__(self, CHANNEL: str, OAUTH_TOKEN:str="SCHMOOPIIE", NICKNAME:str=f"justinfan{random.randint(10000, 99999)}", twitch_irc_capability_tags:bool = False):
        self.CHANNEL = "#" + CHANNEL
        self.OAUTH_TOKEN = OAUTH_TOKEN
        self.NICKNAME = NICKNAME
        self.message_handler_function = None
        self.thread = threading.Thread(target=self._run_loop)
        self._stop_requested = threading.Event()  # Use an event for stopping
        self._disconnect_timeout = 1 # seconds
        self.connected = False

        ### Optional tagging
        self.twitch_irc_capability_tags = twitch_irc_capability_tags
        self.verbose_sysmessages = False
        self.unhandled_message_handler = None 

    def set_client_message_handler(self, handler: Union[Callable[[str, str], None],Callable[[str, str, dict], None]]):
        """
        Sets the message handler function to pass the message data to
        Expects a function with arg1 = username arg2 = message
        Alternatively when using the tags capability arg3 = tags_dict
        """
        self.message_handler_function = handler

    def set_unhandled_message_handler(self, handler: Union[Callable[[str],None], None]) -> None:
        """
        Setting this is optional. This function is used for setting the function that is supposed to recive all the messages that are not caught by this class itself. It is mainly used for debugging.
        """
        self.unhandled_message_handler = handler

    async def messagehandler(self, message_input: str) -> None:
        if not self.twitch_irc_capability_tags: # simpler case
            match = re.match(r"^:(\w+)!\w+@\w+.tmi.twitch.tv PRIVMSG #\w+ :(.*)\r\n$", message_input)
            if match:
                username = match.group(1)
                message = match.group(2)
                self.message_handler_function(username, message)
        else:
            match = re.match(r"^@(.*?)(?: |$):(\w+)!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :(.*)\r\n", message_input)
            if match:
                tags = match.group(1)
                parsed_tags = self.twitch_taghandler(tags)
                username = match.group(2)
                message = match.group(3)
                self.message_handler_function(username, message, parsed_tags)
        if not match: # not a standard message
            if self.verbose_sysmessages: print(message_input) # debugging output
            ping = re.match(r"^PING :(\w+(?:\.\w+)+)", message_input) # keepalive message
            if ping:
                await self.ws.send(f"PONG :{ping.group(1)}")
            elif self.unhandled_message_handler:
                self.unhandled_message_handler(message_input)

    def twitch_taghandler(self, tagstring:str) -> dict:
        """
        Parse the irc twitch tags from string to a dict
        """
        response = {}
        search = re.finditer(r"([\w\-]+)=([\w/#:-]+|)?;?", tagstring)
        for match in search:
            response[match.group(1)] = match.group(2)
        return response

    async def join_chat(self):
        async with websockets.connect(f"wss://irc-ws.chat.twitch.tv:443") as self.ws:
            self.connected = True
            if self.twitch_irc_capability_tags:
                await self.ws.send("CAP REQ :twitch.tv/commands twitch.tv/tags")
            await self.ws.send(f"PASS oauth:{self.OAUTH_TOKEN}")
            await self.ws.send(f"NICK {self.NICKNAME}")
            await self.ws.send(f"JOIN {self.CHANNEL}")

            while not self._stop_requested.is_set():
                try:
                    try:
                        message = await asyncio.wait_for(self.ws.recv(), timeout=self._disconnect_timeout)  # Add a timeout (the time it would wait for a message before checking if a disconnect has been requested)
                    except asyncio.TimeoutError:
                        pass  # Continue the loop if no message is received within the timeout
                    else:
                        await self.messagehandler(message)
                except websockets.exceptions.ConnectionClosedError: ### I have no idea, how the code is supposed to save itself from this
                    self.connected = False
                    print("Connection closed, attempting to reconnect")
                    await asyncio.sleep(5)
            await self.ws.send("PART")
            await self.ws.close()
            self.connected = False

    async def _start_loop(self):
        self.connected = True
        await self.join_chat()

    def _run_loop(self):
        asyncio.run(self._start_loop())

    def start(self):
        """
        Can only be called once per object, it is recomended to destroy the object after calling stop
        """
        self.thread.start()

    def stop(self):
        """
        Calling this function has a (high) possibility to hang the main thread for the maximum of self._disconnect_timeout seconds
        """
        self._stop_requested.set()
        self.thread.join(timeout=self._disconnect_timeout)

def example_chat_handler(uname: str, msg: str, tags:dict = {}) -> None:
    print(f"{uname}: {msg}")
    ### This part is completely optional and can only run when twitch_irc_capability_tags
    if len(tags) > 0 :
        for tag, value in tags.items():
            print(f"{tag}: {value}\t", end="")
        print()


def main():
    tc = TwitchChatListener("goldenbeaster")
    tc.set_client_message_handler(example_chat_handler)
    tc.start()

    # Run your other blocking code here
    time.sleep(10)

    tc.stop()

if __name__ == "__main__":
    main()
