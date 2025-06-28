import shutil
import sys
import os

try:
    from .modules import loadCredentials, wireguradGenerateConfig, loadSettings, downWireguard, upWireguard
except ImportError:
    from modules import loadCredentials, wireguradGenerateConfig, loadSettings, downWireguard, upWireguard

from .vars import _CREDENTIALS_PATH

def blockPeer(name):
    for peer in os.listdir(_CREDENTIALS_PATH):
        if peer == name:
            original_path = os.path.join(_CREDENTIALS_PATH, peer)
            blocked_path = os.path.join(_CREDENTIALS_PATH, f"blocked_{peer}")

            shutil.move(original_path, blocked_path)

            wireguradGenerateConfig(
                config=loadSettings(),
                credentials=loadCredentials(exclude_dirs=("blocked_",)),
            )
            downWireguard()
            upWireguard()
            print(f"[+] Peer '{name}' has been blocked.")
            return

    print(f"[!] Peer '{name}' not found.")