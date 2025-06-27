import os
import json
import sys
import shutil

try:
    from .generate_credentials import generateCredentials
except ImportError:
    from generate_credentials import generateCredentials

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from variables import _CREDENTIALS_PATH

def loadCredentials():
    
    credentials_found = {}

    for client in os.listdir(_CREDENTIALS_PATH):
        absolute_path = os.path.join(_CREDENTIALS_PATH, client)

        privatekey_path = os.path.join(absolute_path, "privatekey")
        with open(privatekey_path, "r") as f:
            privatekey = f.read()

        publickey_path = os.path.join(absolute_path, "publickey")
        with open(publickey_path , "r") as f:
            publickey = f.read()

        credentials_found[client] = {
                "privatekey" : privatekey,
                "publickey" : publickey
            }

    return credentials_found

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print(f"usage {os.path.basename(__file__)} <clients>")
        sys.exit()

    if not sys.argv[1].isdigit():
        print("[-] First arguments must be a integer.")
        sys.exit()

    if os.path.exists(_CREDENTIALS_PATH):
        shutil.rmtree(_CREDENTIALS_PATH)

    os.mkdir(_CREDENTIALS_PATH)

    for index in range(int(sys.argv[1])):

        generateCredentials(
            os.path.join(_CREDENTIALS_PATH,f"peer{index}")
            )


    print(
        json.dumps(
            loadCredentials(),
            indent=2,
        )
    )

