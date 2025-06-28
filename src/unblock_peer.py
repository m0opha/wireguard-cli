import shutil
import sys
import os

try:
    from .modules import loadCredentials , wireguradGenerateConfig , loadSettings , downWireguard , upWireguard
except ImportError:
    from modules import loadCredentials , wireguradGenerateConfig , loadSettings , downWireguard , upWireguard
    
from ..vars import _CREDENTIALS_PATH

def unblockPeer(name):
    blocked_dir = f"blocked_{name}"
    for peer in os.listdir(_CREDENTIALS_PATH):
        if peer == blocked_dir:
            original_path = os.path.join(_CREDENTIALS_PATH, peer)
            restored_path = os.path.join(_CREDENTIALS_PATH, name)

            shutil.move(original_path, restored_path)

            wireguradGenerateConfig(
                config=loadSettings(),
                credentials=loadCredentials(exclude_dirs=("blocked_")),
            )

            print(f"[+] Peer '{name}' has been unblocked.")
            downWireguard()
            upWireguard()
            return

    print(f"[!] Blocked peer '{name}' not found.")
