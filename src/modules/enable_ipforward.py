import os
import subprocess
import sys

_sysctl_config_file_path = "/etc/sysctl.conf"
_sudo_binary_path = "/usr/bin/sudo"
_sysctl_binary_path = "/usr/sbin/sysctl"  # sysctl usualmente está en /usr/sbin

def enableIpForward():
    target_argument = "net.ipv4.ip_forward=1"

    with open(_sysctl_config_file_path, "r") as f:
        sysctl_configuration = f.read().splitlines()

    found = False
    for i, line in enumerate(sysctl_configuration):
        clean_line = line.strip().replace(" ", "")
        if clean_line.startswith("net.ipv4.ip_forward"):
            sysctl_configuration[i] = target_argument
            found = True
            break

    if not found:
        sysctl_configuration.append(target_argument)

    with open(_sysctl_config_file_path, "w") as f:
        f.write("\n".join(sysctl_configuration) + "\n")

    # Aplicar los cambios con sysctl
    result = subprocess.run(
        [_sudo_binary_path, _sysctl_binary_path, "-p"],
        capture_output=True,
        text=True
    )

    if "net.ipv4.ip_forward = 1" in result.stdout:
        print("[+] IP forwarding enabled successfully.")
    else:
        print("[-] Failed to enable IP forwarding.")
        print(result.stdout)
        sys.exit(1)

if __name__ == "__main__":
    enableIpForward()

