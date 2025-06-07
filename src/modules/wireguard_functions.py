import subprocess

def startWireguard():
    # Intentar levantar la interfaz
    wg_quick = subprocess.run(["wg-quick", "up", "wg0"], capture_output=True, text=True)
    if wg_quick.returncode != 0:
        print("[!] Error al levantar wg0 con wg-quick:")
        print(wg_quick.stderr.strip())
        return False


def firstStartWireguard():
    print("[*] Levantando el servidor WireGuard...")
    startWireguard()
    
    print("[+] Interfaz wg0 levantada correctamente.")
    # Intentar habilitar el servicio para arranque automático
    print("[*] Habilitando inicio automático con systemd...")
    systemctl = subprocess.run(["systemctl", "enable", "wg-quick@wg0"], capture_output=True, text=True)

    if systemctl.returncode != 0:
        print("[!] Error al habilitar el servicio wg-quick@wg0:")
        print(systemctl.stderr.strip())

        # Reversión: bajar interfaz si `systemctl enable` falla
        print("[*] Revirtiendo cambios: bajando interfaz wg0...")
        revert = subprocess.run(["wg-quick", "down", "wg0"], capture_output=True, text=True)
        if revert.returncode == 0:
            print("[+] Interfaz wg0 bajada correctamente.")
        else:
            print("[!] Error al bajar wg0 durante la reversión:")
            print(revert.stderr.strip())
        return False

    print("[+] Servicio wg-quick@wg0 habilitado correctamente.")

    return True
