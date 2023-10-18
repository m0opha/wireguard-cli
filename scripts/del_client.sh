#!/bin/bash

root="$(cat ./data/rootpath)"
devices_path="$root/devices"

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 [client name]"
  exit 1 
fi

client_to_delete=$1


if [ ! -d $devices_path/$client_to_delete ]; then
    echo -e "\e[1;31m[-] client not found"
    exit 1
fi

for _device in $(ls $devices_path)
do
    if [ "$_device" == "$client_to_delete" ];then
        rm -r "$devices_path/$_device/"
        rm "$root/wg0.conf"
        break
    fi
done

cat $devices_path/server/wg0.conf > $root/wg0.conf

for _device in $(ls $devices_path); 
do
    if [ "$_device" != "server" ]; then
        echo -e "\n" >> $root/wg0.conf
        cat $devices_path/$_device/server_wg0.conf >> $root/wg0.conf
    fi
done

exit 0