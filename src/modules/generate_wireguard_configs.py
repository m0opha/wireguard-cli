import os
import sys
import json
import shutil

try:
    from .load_credentials import loadCredentials
    from .settings_handler import loadSettings
    from .generate_credentials import generateCredentials

except ImportError:
    from load_credentials import loadCredentials
    from settings_handler import loadSettings
    from generate_credentials import generateCredentials


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from variables import _CREDENTIALS_PATH, _WIREGUARD_ROOT


def genServerConfig(config, credentials):
    return [
        "[Interface]",
        f"Address = {config['range_ip']}/24",
        f"PrivateKey = {credentials['privatekey']}",
        f"ListenPort = {config['listen_port']}",
        f"DNS = {config['dns']}",
        f"PostUp = {config['post_up']}",
        f"PostDown = {config['post_down']}",
        ""
    ]

def generatePeerConfig(peer, config, credentials , server_publickey):
    
    peer_id = int(peer[4:])
    base_ip = ".".join(config['range_ip'].split(".")[:3])
    peer_ip = f"{base_ip}.{peer_id + 2}/32"

    server_peer_config = [
        f"#{peer}",
        "[Peer]",
        f"PublicKey = {credentials['publickey']}",
        f"AllowedIPs = {peer_ip}",
        ""
    ]
    remote_ip = f"{config['remote_ip']}:{config['listen_port']}"

    client_config = [
        "[Interface]",
        f"PrivateKey = {credentials['privatekey']}",
        f"Address = {peer_ip}",
        "",
        "[Peer]",
        f"PublicKey = {server_publickey}",
        f"Endpoint = {remote_ip}",
        f"AllowedIPs = {config['allow_ips']}",
        f"PersistentKeepalive{config['keep_alive']}",
    ]

    return server_peer_config, client_config

def savePeerConfig(peer, config):

    peer_path = os.path.join(_CREDENTIALS_PATH, peer)
    peer_config_path = os.path.join(peer_path, "wg0.conf")

    if not os.path.exists(peer_path):
        os.mkdir(peer_path)
    
    with open(peer_config_path, "w") as f:
            f.write("\n".join(config))

def saveServerConfig(config):
    server_config_path = os.path.join(_WIREGUARD_ROOT, "wg0.conf")
    with open(server_config_path, 'w') as f:
        f.write("\n".join(config))

def genWireguardConfig(config, credentials):

    server_credentials = credentials['server']
    server_config = genServerConfig(config, server_credentials )

    for peer in credentials:

        if peer == "server":
            continue

        peer_credentials = credentials[peer]
        server_peer_config, client_config = generatePeerConfig(
                                                peer=peer,
                                                config=config,
                                                credentials=peer_credentials, 
                                                server_publickey=server_credentials["publickey"]
                                                )
        
        server_config.extend(server_peer_config)
        savePeerConfig(peer, client_config)

    if saveServerConfig(server_config):
        print("[+] Configuración generada y guardada correctamente.")

if __name__ == "__main__":
    if os.path.exists(_CREDENTIALS_PATH):
        shutil.rmtree(_CREDENTIALS_PATH)    
   
    os.mkdir(_CREDENTIALS_PATH)
    
    config = loadSettings()

    generateCredentials(os.path.join(_CREDENTIALS_PATH,"server"))
    for index in range(int(config["peers"])):
        generateCredentials(os.path.join(_CREDENTIALS_PATH,f"peer{index}"))


    credentials = loadCredentials()

    print(
        json.dumps(
            config,
            indent=2
        )
    )
    print( 
        json.dumps(
            credentials,
            indent=2
        )
    )
    



    genWireguardConfig(config, credentials)

