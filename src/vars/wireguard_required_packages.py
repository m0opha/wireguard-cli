WIREGUARD_REQUIRED_PACKAGES = {
    "arch": [
        "wireguard-tools",
        "python-virtualenv",
        "openresolv",
        "iptables",
        "qrencode"
    ],

    "manjaro": [
        "wireguard-tools",
        "python-virtualenv",
        "openresolv",
        "iptables",
        "qrencode"
    ],

    "ubuntu": [
        "wireguard",
        "python3-virtualenv",
        "resolvconf",
        "iptables",
        "qrencode"
    ],

    "debian": [
        "wireguard",
        "python3-virtualenv",
        "resolvconf",
        "iptables",
        "qrencode"
    ],

    "linuxmint": [
        "wireguard",
        "python3-virtualenv",
        "resolvconf",
        "iptables",
        "qrencode"
    ],

    "pop": [
        "wireguard",
        "python3-virtualenv",
        "resolvconf",
        "iptables",
        "qrencode"
    ],

    "fedora": [
        "wireguard-tools",
        "python3-virtualenv",
        "openresolv",
        "iptables",
        "qrencode"
    ],

    "centos": [
        "epel-release",
        "wireguard-tools",
        "python3-virtualenv",
        "openresolv",
        "iptables",
        "qrencode"
    ],

    "rhel": [
        "epel-release",
        "wireguard-tools",
        "python3-virtualenv",
        "openresolv",
        "iptables",
        "qrencode"
    ],

    "opensuse-leap": [
        "wireguard-tools",
        "python3-virtualenv",
        "openresolv",
        "iptables",
        "qrencode"
    ],

    "opensuse-tumbleweed": [
        "wireguard-tools",
        "python3-virtualenv",
        "openresolv",
        "iptables",
        "qrencode"
    ],

    "alpine": [
        "wireguard-tools",
        "py3-virtualenv",
        "openresolv",
        "iptables",
        "qrencode"
    ],

    "void": [
        "wireguard-tools",
        "python3-virtualenv",
        "resolvconf",  # Aquí conviene validar en tu sistema si usar 'resolvconf' o 'openresolv'
        "iptables",
        "qrencode"
    ],

    "gentoo": [
        "net-vpn/wireguard-tools",
        "dev-python/virtualenv",
        "net-dns/openresolv",
        "net-firewall/iptables",
        "media-gfx/qrencode"
    ],

    "nixos": [
        "wireguard-tools",
        "python3Packages.virtualenv",
        # "resolvconf" eliminado porque no existe en nixos
        "iptables",
        "qrencode"
    ],
}
