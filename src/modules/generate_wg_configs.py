import os
import qrcode

from ..vars.paths import (
    _server_credentials_path,
    _wireguard_config_path
)

def validateConfig(config, credentials):
    required_config_keys = ['range_ip', 'listen_port', 'dns', 'PostUp', 'PostDown', 'remote_ip']
    
    for key in required_config_keys:
        if key not in config:
            raise ValueError(f"Falta la clave requerida en config: {key}")

    if 'server' not in credentials or 'privatekey' not in credentials['server']:
        raise ValueError("Faltan credenciales del servidor o su clave privada.")


def generateServerConfig(config, credentials):
    return [
        "[Interface]",
        f"Address = {config['range_ip']}/24",
        f"PrivateKey = {credentials['server']['privatekey']}",
        f"ListenPort = {config['listen_port']}",
        f"DNS = {config['dns']}",
        f"PostUp = {config['PostUp']}",
        f"PostDown = {config['PostDown']}",
        ""
    ]


def generatePeerConfig(_peer, config, credentials):
    try:
        id_peer = int(_peer[4:]) + 1
    
    except ValueError:
        print(f"Nombre de peer inválido (esperado 'peerN'): {_peer}")
        return None, None

    base_ip_parts = config['range_ip'].split(".")
    if len(base_ip_parts) != 4:
        print(f"IP base inválida: {config['range_ip']}")
        return None, None

    base_ip = ".".join(base_ip_parts[:3])
    peer_ip = f"{base_ip}.{id_peer}/32"

    server_peer_block = [
        f"#{_peer}",
        "[Peer]",
        f"PublicKey = {credentials[_peer]['publickey']}",
        f"AllowedIPs = {peer_ip}",
        ""
    ]

    client_config = [
        "[Interface]",
        f"PrivateKey = {credentials[_peer]['privatekey']}",
        f"Address = {peer_ip}",
        "",
        "[Peer]",
        f"PublicKey = {credentials['server']['publickey']}",
        f"Endpoint = {config['remote_ip']}:{config['listen_port']}",
        "AllowedIPs = 0.0.0.0/0",
        "PersistentKeepalive = 25",
    ]

    return server_peer_block, client_config


def saveClientConfig(_peer, client_lines):
    client_path = os.path.join(_server_credentials_path, _peer)
    os.makedirs(client_path, exist_ok=True)

    conf_path = os.path.join(client_path, "wg0.conf")
    try:
        with open(conf_path, "w") as f:
            f.write("\n".join(client_lines) + "\n")
    except IOError as e:
        print(f"Error al escribir configuración de {_peer}: {e}")
        return

    try:
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q)
        qr.add_data("\n".join(client_lines))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(os.path.join(client_path, "wg0.png"))
    except Exception as e:
        print(f"Error al generar QR para {_peer}: {e}")


def saveServerConfig(server_lines):
    os.makedirs(_wireguard_config_path, exist_ok=True)
    server_conf_path = os.path.join(_wireguard_config_path, "wg0.conf")
    try:
        with open(server_conf_path, 'w') as f:
            f.write("\n".join(server_lines) + "\n")
    except IOError as e:
        print(f"Error al escribir configuración del servidor: {e}")
        return False
    return True


def generateWgConfigs(config, credentials):
    validateConfig(config, credentials)
    server_lines = generateServerConfig(config, credentials)

    for _peer in credentials:
        if _peer == "server":
            continue

        if 'privatekey' not in credentials[_peer] or 'publickey' not in credentials[_peer]:
            print(f"Credenciales incompletas para {_peer}. Saltando.")
            continue

        server_peer_block, client_config = generatePeerConfig(_peer, config, credentials)
        if not server_peer_block or not client_config:
            continue

        server_lines.extend(server_peer_block)
        saveClientConfig(_peer, client_config)

    if saveServerConfig(server_lines):
        print("[+] Configuración generada y guardada correctamente.")
