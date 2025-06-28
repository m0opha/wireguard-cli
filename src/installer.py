import os
import shutil
import json
import sys

try:
    from .modules import *
    from .interface import install_interface
    from .vars import _CREDENTIALS_PATH, _WIREGUARD_ROOT


except ImportError:
    from modules import *
    from interface import install_interface
    from vars import _CREDENTIALS_PATH, _WIREGUARD_ROOT
    

def confirm_and_reset_credentials(path: str):
    if os.path.exists(path):
        choice = input("[*] Existing credentials will be deleted. Continue? (Y/N): ")
        if choice.lower().startswith("y"):
            shutil.rmtree(path)
            os.mkdir(path)
            print("[+] Credentials directory has been reset.")
            return

        print("[-] Installation canceled.")
        sys.exit(0)
    else:
        os.mkdir(_CREDENTIALS_PATH)

def generatePeerCredentials(peers:int):
    for p in range(peers):
        credentialsGenerator(os.path.join(_CREDENTIALS_PATH,f"peer{p}"))

import os
import subprocess

def generateResolvConf():
    resolv_path = "/etc/resolv.conf"

    # Si no existe o es un enlace roto, intentar regenerarlo
    if not os.path.exists(resolv_path) or os.path.islink(resolv_path) and not os.path.exists(os.readlink(resolv_path)):
        print("[*] Attempting to update /etc/resolv.conf using resolvconf...")
        result = subprocess.run(
            ["resolvconf", "-u"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("[+] /etc/resolv.conf updated successfully.")
        else:
            print("[-] Failed to update /etc/resolv.conf")
            print(f"stderr: {result.stderr.strip()}")

    else:
        print("[i] /etc/resolv.conf already exists.")

def installer():
    #wireguard installation
    installWireguard()

    #enable ip forwarding
    ipForwardHandler()

    #config dir
    confirm_and_reset_credentials(_CREDENTIALS_PATH)

    #get config from user
    config = install_interface()
    
    #save settings given
    saveSettings(config)
    
    #create proyect config directory
    configDirectory()

    #set permissions
    setPermissions(_WIREGUARD_ROOT, 0o700) 
    
    #generate credentials
    generatePeerCredentials(int(config["peers"]))
    credentialsGenerator(os.path.join(_CREDENTIALS_PATH , "server"))

    #load all credentials
    all_credentials = loadCredentials()

    #wireguard gen wg0.conf files
    wireguradGenerateConfig(config, all_credentials)

    #enable and start wireguard
    enableWireguard()
    upWireguard()

    print("[!] installation done.")

if __name__ == "__main__":
    installer()
