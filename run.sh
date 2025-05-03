#!/bin/bash

# Paso 1: Actualizar el sistema
echo "[*] Actualizando y mejorando el sistema..."
sudo apt update && sudo apt upgrade -y

# Paso 2: Instalar paquetes necesarios
echo "[*] Instalando WireGuard, python3-virtualenv, ufw, resolvconf, iptables..."
sudo apt install -y wireguard python3-virtualenv ufw resolvconf iptables qrencode

# Verificar si OpenSSH está permitido en UFW antes de habilitarlo
echo "[*] Verificando si SSH está permitido en UFW..."

# Comprobar si OpenSSH está habilitado en UFW
if ! sudo ufw app list | grep -q "OpenSSH"
then
    echo "[!] SSH no está permitido en UFW. Lo habilitaremos ahora (puerto 22/tcp)."
    sudo ufw allow 22/tcp  # Permitir el puerto 22 para SSH
else
    echo "[+] SSH ya está permitido en UFW."
fi

# Abrir puerto UDP de WireGuard (por defecto 51820)
sudo ufw allow 51820/udp

# Paso 4: Habilitar UFW
echo "[*] Habilitando UFW..."
sudo ufw enable

# Verificar estado de UFW
echo "[*] Verificando estado de UFW..."
sudo ufw status verbose

# Paso 5: Comprobación de instalación de WireGuard
echo "[*] Verificando si WireGuard está instalado correctamente..."
if ! command -v wg &> /dev/null
then
    echo "[!] Error: WireGuard no se instaló correctamente."
    exit 1
else
    echo "[+] WireGuard instalado correctamente."
fi

# Paso 6: Verificar si resolvconf está activo
echo "[*] Verificando si resolvconf está activo..."
if ! systemctl is-active --quiet resolvconf
then
    echo "[!] Resolving: resolvconf no está activo. Asegúrate de que el servicio esté habilitado."
else
    echo "[+] Resolvconf activo correctamente."
fi

# Paso 7: Comprobar iptables
echo "[*] Verificando si iptables está instalado..."
if ! command -v iptables &> /dev/null
then
    echo "[!] Error: iptables no está instalado correctamente."
    exit 1
else
    echo "[+] iptables está disponible."
fi

echo "[+] ¡Todo listo! WireGuard y configuraciones de firewall instaladas correctamente."

virtualenv .env
source .env/bin/activate
pip install pyinstaller pillow qrcode
python3 wireguard-cli.py
deactivate
