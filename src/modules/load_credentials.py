import os
import json
import sys
import shutil

try:
    from .credentials_generator import credentialsGenerator
except ImportError:
    from credentials_generator import credentialsGenerator

from vars import _CREDENTIALS_PATH, debug


def loadCredentials(target_startwith="peer", exclude_dirs=()):
    credentials_found = {}

    if not os.path.exists(_CREDENTIALS_PATH):
        return {}

    for client in os.listdir(_CREDENTIALS_PATH):
        if (
            client != "server"
            and not client.startswith(target_startwith)
            or any(client.startswith(prefix) for prefix in exclude_dirs)
        ):
            continue

        absolute_path = os.path.join(_CREDENTIALS_PATH, client)

        privatekey_path = os.path.join(absolute_path, "privatekey")
        publickey_path = os.path.join(absolute_path, "publickey")

        # ⚠️ Crear las credenciales si faltan
        if not (os.path.exists(privatekey_path) and os.path.exists(publickey_path)):
            if debug:
                print(f"[!] Missing credentials for {client}, generating...")
            credentialsGenerator(absolute_path)

        try:
            with open(privatekey_path, "r", encoding="utf-8") as f:
                privatekey = f.read().strip()

            with open(publickey_path, "r", encoding="utf-8") as f:
                publickey = f.read().strip()

            credentials_found[client] = {
                "privatekey": privatekey,
                "publickey": publickey
            }

        except Exception as e:
            if debug:
                print(f"[!] Failed to load credentials for {client}: {e}")
            continue

    return dict(sorted(credentials_found.items()))


if __name__ == "__main__" and debug:
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

        credentialsGenerator(
            os.path.join(_CREDENTIALS_PATH,f"peer{index}")
            )


    print(
        json.dumps(
            loadCredentials(),
            indent=2,
        )
    )

