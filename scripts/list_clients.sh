root="/etc/wireguard"

devices_path="$root/devices"

for _client in $(ls $devices_path); do
        if [ "$_client" != "server" ]; then
                echo -e " \e[1;32m[+] $_client"
        fi
done
