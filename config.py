import json
import os

CONFIG_PATH = "tts_config.json"

DEFAULT_CONFIG = {
    "open_hotkey": "enter",
    "quick_messages": {
        "F3": "??",
        "F4": "??",
        "F5": "??",
        "F6": "??",
        "F7": "??"
    }
}

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

config = load_config()
OPEN_HOTKEY = config["open_hotkey"]
QUICK_MSGS = config["quick_messages"]