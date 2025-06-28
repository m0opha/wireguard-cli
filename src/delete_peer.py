import os
import sys
import shutil

from .modules import (
    loadSettings,
    loadCredentials,
    wireguradGenerateConfig,
    downWireguard,
    upWireguard
)

from .vars import _CREDENTIALS_PATH

def deletePeer(name):
    peer_path = os.path.join(_CREDENTIALS_PATH, name)

    if not os.path.exists(peer_path):
        print(f"[!] Peer '{name}' not found.")
        return

    try:
        shutil.rmtree(peer_path)
        print(f"[+] Peer '{name}' deleted.")
    except Exception as e:
        print(f"[!] Error deleting peer '{name}': {e}")
        return

    # Regenerar configuración y reiniciar interfaz
    wireguradGenerateConfig(
        config=loadSettings(),
        credentials=loadCredentials(exclude_dirs=("blocked_",))
    )
    downWireguard()
    upWireguard()
