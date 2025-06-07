#!/bin/bash

echo "[*] Actualizando y mejorando el sistema..."
sudo apt update && sudo apt upgrade -y


echo "[*] Instalando WireGuard, python3-virtualenv, ufw, resolvconf, iptables..."
sudo apt install -y wireguard python3-virtualenv resolvconf iptables qrencode


#echo "[*] Abriendo puerto SSH en UFW..."
#sudo ufw allow 22/tcp
#
#
#echo "[*] Abriendo puerto Wireguard en UFW..."
#sudo ufw allow 51820/udp
#
#
#echo "[*] Habilitando UFW..."
#sudo ufw enable
#
#
#echo "[*] Verificando estado de UFW..."
#sudo ufw status verbose


echo "[*] Verificando si WireGuard está instalado correctamente..."
if ! command -v wg &> /dev/null
then
    echo "[!] Error: WireGuard no se instaló correctamente."
    exit 1
fi
echo "[+] WireGuard instalado correctamente."


echo "[*] Verificando si resolvconf está activo..."
if ! systemctl is-active --quiet resolvconf
then
    echo "[!] Resolving: resolvconf no está activo. Asegúrate de que el servicio esté habilitado."
    exit 1
fi
echo "[+] Resolvconf activo correctamente."


echo "[*] Verificando si iptables está instalado..."
if ! command -v iptables &> /dev/null
then
    echo "[!] Error: iptables no está instalado correctamente."
    exit 1
fi
echo "[+] iptables está disponible."

echo "[+] ¡Todo listo! WireGuard y configuraciones de firewall instaladas correctamente."

virtualenv .env
source .env/bin/activate
pip install pyinstaller pillow qrcode
python3 wireguard-cli.py
deactivate