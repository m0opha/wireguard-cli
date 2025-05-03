
from .vars.paths import _server_credentials_path, _app_config_path

from .modules.generate_credentials import generateCredentials
from .modules.load_credentials import loadCredentials
from .modules.generate_wg_configs import generateWgConfigs

def createPeer():
    pass