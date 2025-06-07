import os
import shutil
import json
import sys

from .vars.paths import (
    _server_credentials_path,
    _wireguard_config_path,
    _app_config_path
)

from .modules.generate_wg_configs import generateWgConfigs
from .modules.generate_credentials import generateCredentials
from .modules.create_config_directory import createConfigDirectory
from .modules.check_permissions import checkPermissions
from .modules.load_credentials import loadCredentials
from .modules.enable_ipforward import enableIpForward
from .modules.wireguard_functions import firstStartWireguard

from .interface.initialize_interface import initializeInterface

def installer():
    # Paso 1: Inicializar configuración de WireGuard
    wg_config = initializeInterface()

    # Paso 2: Confirmar eliminación de credenciales previas
    if os.path.exists(_server_credentials_path):
        op = input("[*] Se eliminarán las credenciales anteriores. ¿Continuar? (Y/N): ")
        if op.lower() == "y":
            shutil.rmtree(_server_credentials_path)
            os.mkdir(_server_credentials_path)
        else:
            print("Instalación cancelada.")
            sys.exit(0)

    # Paso 3: Crear estructura de carpetas y asegurar permisos
    createConfigDirectory()
    checkPermissions(_wireguard_config_path, 0o700)

    # Paso 4: Guardar configuración en archivo
    try:
        os.makedirs(_app_config_path, exist_ok=True)
        with open(os.path.join(_app_config_path, "configuration.json"), "w") as f:
            json.dump(wg_config, f, indent=4)
    except Exception as e:
        print(f"Error al guardar la configuración: {e}")
        sys.exit(1)

    # Paso 5: Generar credenciales (servidor + peers)
    generateCredentials("server")
    for _peer in range(wg_config["peers"]):
        generateCredentials(f"peer{_peer + 1}")


    # Paso 6: Cargar credenciales generadas
    try:
        all_credentials = loadCredentials()
    except Exception as e:
        print(f"Error al cargar credenciales: {e}")
        sys.exit(1)

    # Paso 7: Generar archivos de configuración
    try:
        generateWgConfigs(wg_config, all_credentials)
    except Exception as e:
        print(f"Error al generar configuraciones de WireGuard: {e}")
        sys.exit(1)

    # Paso 8: Activar IP forwarding
    enableIpForward()

    # Paso 9: Levantar el servidor wireguard
    if not firstStartWireguard():
        print("[!] No se pudo iniciar WireGuard correctamente.")
        sys.exit(1)
    else:
        print("[+] WireGuard está corriendo y listo.")

    print("[+] Instalación completa.")

if __name__ == "__main__":
    installer()
