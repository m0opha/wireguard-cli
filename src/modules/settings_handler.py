import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from variables import _SETTINGS_FILE_PATH

def loadSettings():
    try:
        with open(_SETTINGS_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {} 

def saveSettings(data: dict):
    try:
        with open(_SETTINGS_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        return False
