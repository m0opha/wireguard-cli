root="/etc/wireguard"

devices_path="$root/devices"

for _client in $(ls $devices_path); do
        echo -e " \e[1;31m[+] $_client"
done
