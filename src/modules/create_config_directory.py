import os

from ..vars.paths import _wireguard_config_path

def createConfigDirectory():
    path = os.path.join(_wireguard_config_path, "configs")
    try:
        os.makedirs(path, exist_ok=True)
        print(f"[+] Directorio de configuracion creado")

    except PermissionError:
        print(f"[-] Permiso denegado al crear el directorio: {path}")
    except OSError as e:
        print(f"[-] Error al crear el directorio {path}: {e}")
