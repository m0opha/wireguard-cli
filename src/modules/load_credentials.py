import os

from ..vars.paths import _server_credentials_path

def loadCredentials():
    
    credentials = {}

    for _client in os.listdir(_server_credentials_path):
        full_path = os.path.join(_server_credentials_path, _client)
        
        privatekey_path = os.path.join(full_path, "privatekey")
        with open(privatekey_path, "r") as f:
            privatekey = f.read()

        publickey_path = os.path.join(full_path, "publickey")
        with open(publickey_path , "r") as f:
            publickey = f.read()

        credentials[_client] = {
                "privatekey" : privatekey,
                "publickey" : publickey
            }

    return credentials