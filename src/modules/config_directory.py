import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from variables import _PROJECT_CONFIG_PATH

def configDirectory():
    if not os.path.exists(_PROJECT_CONFIG_PATH):
        os.mkdir(_PROJECT_CONFIG_PATH)
        print(f"[+] Config directory has been created.")

if __name__ == "__main__":
    configDirectory()