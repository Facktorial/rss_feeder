from my_types import PostRecord, FeedRecord, Sandbox
from xml_feeder import filtred_feeder
from links_parser import links_from_json
from typing import List, Set
from app_tui import render, clearConsole

from pynput.keyboard import Listener, Key

import asyncio
import time


def on_press(key, data, sandbox) -> bool:
    if key == Key.esc:
        return False
    elif key == Key.left:
        if (sandbox.cursor_pos > 0):
            sandbox.cursor_pos = sandbox.cursor_pos - 1
            render(data, sandbox)
        return True
    elif key == Key.right:
        if (sandbox.cursor_pos < len(sandbox.topics) - 1):
            sandbox.cursor_pos = sandbox.cursor_pos + 1
            render(data, sandbox)
        return True

def app():
    sandbox = Sandbox(0)

    data, topics = asyncio.run(filtred_feeder(links_from_json('RSS_feeds.json'), days=28, sandbox=sandbox))

    sandbox.topics = list(topics)
    # sandbox.cursor_pos = sandbox.topics.index("Haskell")
    sandbox.cursor_pos = sandbox.topics.index(sorted(topics)[0])

    render(data, sandbox)
    with Listener(on_press=lambda event: on_press(event, data, sandbox)) as listener:
        listener.join()

if __name__ == "__main__":
    app()
    # curses.wrapper(scr)
