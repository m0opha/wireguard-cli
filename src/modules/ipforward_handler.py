import os
import subprocess
import sys
import re


try:
    from .get_binary_path import getBinaryPath

except ImportError:
    from get_binary_path import getBinaryPath

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from variables import _SYSCTL_CONFIG_FILE_PATH, debug

_TARGET_ARGUMENT = "net.ipv4.ip_forward"

def ipForwardHandler(enable=True,set_config=True):
    SUDO_BINARY = getBinaryPath("sudo")[0]
    SYSCTL_BINARY = getBinaryPath("sysctl")[0]

    with open(_SYSCTL_CONFIG_FILE_PATH, "r") as f:
        sysctl_configuration = f.read().splitlines()

    found = False
    for i, line in enumerate(sysctl_configuration):
        clean_line = re.sub(r'[#\s]', '', line.strip())

        if clean_line.startswith(_TARGET_ARGUMENT):
            
            sysctl_configuration[i] = _TARGET_ARGUMENT + "=1" if enable else _TARGET_ARGUMENT + "=0"
            found = True
            break

    if not found:
        sysctl_configuration.append(_TARGET_ARGUMENT + "=1" if enable else _TARGET_ARGUMENT + "=0")


    with open(_SYSCTL_CONFIG_FILE_PATH, "w") as f:
        f.write("\n".join(sysctl_configuration))

    if set_config:
        result = subprocess.run(
            [SUDO_BINARY, SYSCTL_BINARY, "-p"],
            capture_output=True,
            text=True
        )

        if not "net.ipv4.ip_forward = 1" in result.stdout:
            print("[-] Failed to enable IP forwarding.")
            return

        print("[+] IP forwarding enabled successfully.")

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print(f"usage: {os.path.basename(__file__)} <enable or disable>")
        sys.exit(0)

    option = sys.argv[1]
    enable=True

    if option == "disable":
        enable=False

    if debug:
        if not os.path.exists(_SYSCTL_CONFIG_FILE_PATH):
            with open(_SYSCTL_CONFIG_FILE_PATH, "w") as f:
                pass

        ipForwardHandler(enable=enable, set_config=False)

        with open(_SYSCTL_CONFIG_FILE_PATH, "r") as sysctl_conf:
            print(sysctl_conf.read())

        sys.exit(0)


    ipForwardHandler(enable=enable)