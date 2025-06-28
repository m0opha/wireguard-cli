import os
import ipaddress
import subprocess
import re
DEFAULTS = {
    "range_ip": "10.0.0.1/24",
    "listen_port": "51820",
    "remote_ip": "10.0.0.2",
    "interface": "wg0",
    "post_up": "iptables -A FORWARD -i %i -j ACCEPT",
    "post_down": "iptables -D FORWARD -i %i -j ACCEPT",
    "dns": "1.1.1.1",
    "peers": "3",
    "allow_ips": "0.0.0.0/0",
    "keep_alive": "25"
}

def get_public_ip_curl():
    try:
        result = subprocess.run(
            ["curl", "-s", "ifconfig.me"],
            capture_output=True,
            text=True,
            timeout=5
        )
        ip = result.stdout.strip()
        if ip:
            return ip
    except Exception as e:
        print(f"[!] Could not get public IP via curl: {e}")
    return ""

def list_network_interfaces():
    net_path = '/sys/class/net'
    if not os.path.exists(net_path):
        return []
    return [iface for iface in os.listdir(net_path) if iface != 'lo']

def ask(field, default):
    while True:
        value = input(f"{field} [{default}]: ").strip()
        if not value:
            return default
        return value

def ask_interface(default):
    interfaces = list_network_interfaces()
    if not interfaces:
        print("No network interfaces found, using default.")
        return default

    print("Available network interfaces:")
    for i, iface in enumerate(interfaces, start=1):
        print(f"  {i}. {iface}")

    while True:
        choice = input(f"Select interface by number or name [{default}]: ").strip()
        if not choice:
            return default
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(interfaces):
                return interfaces[idx]
        elif choice in interfaces:
            return choice
        print("[!] Invalid choice, please try again.")

def is_valid_ip_or_domain(value: str) -> bool:
    # Check if it's a valid IP address
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        pass

    # Check if it's a valid domain name
    domain_regex = re.compile(
        r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)"
        r"(?:\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*"
        r"\.[A-Za-z]{2,}$"
    )
    return bool(domain_regex.fullmatch(value))

def is_valid_network(ip_range):
    try:
        ipaddress.ip_network(ip_range, strict=False)
        return True
    except ValueError:
        return False

def install_interface():
    config = {}
    print("----------------------------------------------")
    print("Configure your WireGuard interface parameters. \nPress Enter to accept the default.")

    for key, default in DEFAULTS.items():
        while True:
            if key == "interface":
                value = ask_interface(default)
            elif key == "remote_ip":
                value = input(f"{key} [default: detect public IP]: ").strip()
                if not value:
                    value = get_public_ip_curl() or default
                    print(f"    [!] Using detected public IP: {value}")
            else:
                value = ask(key, default)

            # Validate inputs
            if key in ("range_ip", "allow_ips"):
                if not is_valid_network(value):
                    print("[!] Invalid IP range format, try again.")
                    continue
            elif key in ("remote_ip", "dns"):
                if not is_valid_ip_or_domain(value):
                    print("[!] Invalid IP address, try again.")
                    continue
            elif key in ("listen_port", "keep_alive", "peers"):
                if not value.isdigit():
                    print("[!] Must be a number, try again.")
                    continue

            config[key] = value
            break

    if "interface" in config:
        iface = config["interface"]
        config["post_up"] = DEFAULTS["post_up"].replace("%i", iface)
        config["post_down"] = DEFAULTS["post_down"].replace("%i", iface)

    return config


if __name__ == "__main__":
    config = install_interface()
    print("\nGenerated Interface Configuration:\n" + "-" * 32)
    for k, v in config.items():
        print(f"{k}: {v}")
