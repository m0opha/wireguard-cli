import os

_wireguard_config_path = "/etc/wireguard"
_app_config_path = os.path.join(_wireguard_config_path, "configs")
_server_credentials_path = os.path.join(_wireguard_config_path, "credentials")