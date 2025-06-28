import subprocess
import sys
import os

try:
    from .get_binary_path import getBinaryPath

except ImportError:
    from get_binary_path import getBinaryPath

from vars import WIREGUARD_REQUIRED_PACKAGES, debug

def getDistribution():
    os_release = "/etc/os-release"
    try:
        with open(os_release, "r") as f:
            for line in f:
                line = line.strip()
                if not line or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                if key == "ID":
                    return value.strip('"').lower()
    except FileNotFoundError:
        return None
    return None

def detect_distribution_installer(install=True):
    distro = getDistribution()
    sudo = getBinaryPath("sudo")

    if distro in ["arch", "manjaro"]:
        return [sudo, getBinaryPath("pacman"), "-S" if install else "-Rns", "--noconfirm"]
    elif distro in ["ubuntu", "debian", "linuxmint", "pop"]:
        return [sudo, getBinaryPath("apt"), "install" if install else "remove", "-y"]
    elif distro in ["fedora"]:
        return [sudo, getBinaryPath("dnf"), "install" if install else "remove", "-y"]
    elif distro in ["centos", "rhel"]:
        return [sudo, getBinaryPath("yum"), "install" if install else "remove", "-y"]
    elif distro in ["opensuse-leap", "opensuse-tumbleweed"]:
        return [sudo, getBinaryPath("zypper"), "install" if install else "remove", "--non-interactive"]
    elif distro in ["alpine"]:
        return [sudo, getBinaryPath("apk"), "add" if install else "del", "-q", "-y"]
    elif distro in ["void"]:
        return [sudo, getBinaryPath("xbps-install"), "-S" if install else "-R", "-y"]
    elif distro in ["gentoo"]:
        return [sudo, getBinaryPath("emerge"), "--ask" if install else "--unmerge"]
    elif distro in ["nixos"]:
        if install:
            return [sudo, getBinaryPath("nix-env"), "-iA", "nixos."]
        else:
            return [sudo, getBinaryPath("nix-env"), "-e"]
    return None


import subprocess

def distributionPackageHandler(packages: list, install: bool = True, verbose: bool = False):
    for package in packages:
        command = detect_distribution_installer(install=install)
        if not command:
            print("[-] Could not detect package manager command.")
            return

        command.append(package)

        result = subprocess.run(
            command,
            capture_output=not verbose,
            text=True
        )

        if result.returncode == 0:
            action = "installed" if install else "removed"
            print(f"[+] package {package} {action} successfully.")
            if verbose and (result.stdout or result.stderr):
                if result.stdout:
                    print(f"stdout:\n{result.stdout}")
                if result.stderr:
                    print(f"stderr:\n{result.stderr}")
        else:
            action = "install" if install else "remove"
            print(f"[-] package {package} failed to {action}.")
            if verbose and (result.stdout or result.stderr):
                if result.stdout:
                    print(f"stdout:\n{result.stdout}")
                if result.stderr:
                    print(f"stderr:\n{result.stderr}")

def installWireguard(install=True, verbose=False):
    distributionPackageHandler(
        WIREGUARD_REQUIRED_PACKAGES[getDistribution()],
        install=install,
        verbose=verbose,
        )

if __name__ == "__main__" and debug:
    print(repr(getDistribution()))
    print(repr(detect_distribution_installer()))
    installWireguard()

