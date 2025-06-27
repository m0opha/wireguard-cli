import os
import sys
import json
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from variables import (
    _PROJECT_CONFIG_PATH, 
    _SETTINGS_FILE_PATH, 
    settings_content
    )

def configDirectory():
    if not os.path.exists(_PROJECT_CONFIG_PATH):
        os.mkdir(_PROJECT_CONFIG_PATH)
        print(f"[+] Config directory has been created.")

        with open(_SETTINGS_FILE_PATH, "w") as f:
            json.dump(settings_content, f, indent=2)

if __name__ == "__main__":
    if os.path.exists(_PROJECT_CONFIG_PATH):
        shutil.rmtree(_PROJECT_CONFIG_PATH)

    configDirectory()