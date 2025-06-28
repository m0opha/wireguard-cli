import os
import sys
import json
import re
from ipaddress import ip_network, ip_address

from .modules import (
    loadSettings,
    loadCredentials,
    wireguradGenerateConfig,
    downWireguard,
    upWireguard,
    credentialsGenerator,
)

from .vars import _CREDENTIALS_PATH


def getNextAvailablePeerNumber():
    pattern = re.compile(r'^peer(\d+)$')
    existing_numbers = set()

    for peer in os.listdir(_CREDENTIALS_PATH):
        m = pattern.match(peer)
        if m:
            existing_numbers.add(int(m.group(1)))

    n = 1
    while n in existing_numbers:
        n += 1
    return n


def getNextAvailableIP(used_ips, network):
    for ip in network.hosts():
        if ip not in used_ips:
            return str(ip)
    raise RuntimeError("No available IPs in the range")


def createPeer(count=1, forced_number=None):
    config = loadSettings()
    credentials = loadCredentials(exclude_dirs=("blocked_",))
    network = ip_network(config["range_ip"], strict=False)

    used_ips = {
        network.network_address,                         # 10.0.0.0
        ip_address(config["range_ip"].split("/")[0])     # 10.0.0.1 (server)
    }

    for peer in credentials.values():
        try:
            used_ips.add(ip_address(peer["ip"]))
        except:
            continue

    created = 0
    current_number = forced_number or getNextAvailablePeerNumber()

    while created < count:
        peer_name = f"peer{current_number}"
        peer_path = os.path.join(_CREDENTIALS_PATH, peer_name)

        if os.path.exists(peer_path):
            current_number += 1
            continue

        os.mkdir(peer_path)
        credentialsGenerator(peer_path)

        try:
            peer_ip = getNextAvailableIP(used_ips, network)
        except RuntimeError:
            print("[!] No more available IPs.")
            break

        used_ips.add(ip_address(peer_ip))

        # Guardar IP
        data = {
            "name": peer_name,
            "ip": peer_ip
        }
        with open(os.path.join(peer_path, "data.json"), "w") as f:
            json.dump(data, f, indent=2)

        print(f"[+] Created {peer_name} with IP {peer_ip}")

        created += 1
        current_number += 1

    if created > 0:
        wireguradGenerateConfig(
            config=config,
            credentials=loadCredentials(exclude_dirs=("blocked_",))
        )
        downWireguard()
        upWireguard()
