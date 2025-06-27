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

TARGET="peer"
def loadCredentials():
    credentials_found = {}

    if not os.path.exists(_CREDENTIALS_PATH):
        return {}

    for client in os.listdir(_CREDENTIALS_PATH):

        if  client != "server" and not client.startswith(TARGET):
            continue

        absolute_path = os.path.join(_CREDENTIALS_PATH, client)

        privatekey_path = os.path.join(absolute_path, "privatekey")
        publickey_path = os.path.join(absolute_path, "publickey")

        with open(privatekey_path, "r", encoding="utf-8") as f:
            privatekey = f.read()

        with open(publickey_path, "r", encoding="utf-8") as f:
            publickey = f.read()

        credentials_found[client] = {
            "privatekey": privatekey,
            "publickey": publickey
        }


    return dict(sorted(credentials_found.items(), reverse=False))


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

