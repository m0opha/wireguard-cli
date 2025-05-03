import subprocess
import os

from ..vars.paths import _server_credentials_path

def generateCredentials(client: str):
    target_dir = os.path.join(_server_credentials_path, client)
    os.makedirs(target_dir, exist_ok=True)
    
    privatekey = subprocess.run(
        ["wg", "genkey"],
        capture_output=True,
        text=True
    ).stdout.strip()
    
    publickey = subprocess.run(
        ["wg", "pubkey"],
        input=privatekey,
        capture_output=True,
        text=True
    ).stdout.strip()
    
    with open(os.path.join(target_dir, "privatekey"), "w") as f:
        f.write(privatekey)
    
    with open(os.path.join(target_dir, "publickey"), "w") as f:
        f.write(publickey)   

