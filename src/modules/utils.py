import os
import sys
import json

from vars import _SETTINGS_FILE_PATH

def resolvePath(path: str) -> str:
    path = os.path.expanduser(path)    
    path = os.path.abspath(path)
    return path

def setPermissions(path:str, permissions:int):
    currentPermissions = os.stat(path).st_mode
    if oct(currentPermissions)[-3:] != oct(permissions)[-3:]:
        os.chmod(path, permissions)

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