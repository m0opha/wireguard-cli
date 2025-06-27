import os
import sys

try:
    from .configs import debug

except ImportError:
    from configs import debug

#wireguard config path
_WIREGUARD_ROOT = "/etc/wireguard" if not debug else os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")), "docs/wireguard" )

#proyect paths
_PROJECT_CONFIG_PATH = os.path.join(_WIREGUARD_ROOT, "configs")
_SETTINGS_FILE_PATH = os.path.join(_PROJECT_CONFIG_PATH, "settings.json")
_CREDENTIALS_PATH = os.path.join(_WIREGUARD_ROOT ,  "credentials")

#system config paths
_SYSCTL_CONFIG_FILE_PATH = "/etc/sysctl.conf" if not debug else os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")), "docs/sysctl.conf" )

if __name__ == "__main__":
    print(_WIREGUARD_ROOT)
    print(_PROJECT_CONFIG_PATH)
    print(_CREDENTIALS_PATH)