import subprocess

def downWireguard():
    print("[*] Bringing down interface wg0...")
    result = subprocess.run(
        ["sudo", "wg-quick", "down", "wg0"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("[!] Failed to bring down wg0:")
        print(result.stderr.strip())
        return False

    print("[+] Interface wg0 successfully brought down.")
    return True

def upWireguard():
    wg_quick = subprocess.run(
        ["sudo","wg-quick", "up", "wg0"],
        capture_output=True,
        text=True
    )

    if wg_quick.returncode != 0:
        print("[!] Error bringing up wg0 with wg-quick:")
        return False
    
    print("[+] Interface wg0 successfully brought up.")
    return True


def enableWireguard():    
    print("[*] Enabling automatic startup with systemd...")
    result = subprocess.run(
        ["sudo","systemctl", "enable", "wg-quick@wg0"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("[!] Failed to enable wg-quick@wg0 service:")
        print("[*] Rolling back: bringing down wg0...")
        revert = subprocess.run(
            ["sudo","wg-quick", "down", "wg0"], 
            capture_output=True, 
            text=True
        )

        if revert.returncode == 0:
            print("[+] Interface wg0 successfully brought down.")
            return False

        print("[!] Failed to bring down wg0 during rollback:")
        return False

    print("[+] wg-quick@wg0 service enabled successfully.")
    return True
