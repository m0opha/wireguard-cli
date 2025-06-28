import subprocess
import os
import sys

try:
    from .get_binary_path import getBinaryPath

except ImportError:
    from get_binary_path import getBinaryPath
    
from vars import _CREDENTIALS_PATH

def credentialsGenerator(output_path=None):

    WG_BINARY = getBinaryPath("wg")

    privatekey = subprocess.run(
        [WG_BINARY, "genkey"],
        capture_output=True,
        text=True
    ).stdout.strip()
    
    publickey = subprocess.run(
        [WG_BINARY, "pubkey"],
        input=privatekey,
        capture_output=True,
        text=True
    ).stdout.strip()
    
    if output_path:
        if not os.path.exists(output_path):
            os.mkdir(output_path)

        with open(os.path.join(output_path, "privatekey"), "w") as f:
            f.write(privatekey)
    
        with open(os.path.join(output_path, "publickey"), "w") as f:
            f.write(publickey)   
    
    return (privatekey , publickey)

if __name__ == "__main__":
    privatekey , publickey = generateCredentials()
    print(f"Private key: {privatekey}")
    print(f"Public key: {publickey}")