#!/bin/bash

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 [client name]"
  exit 1 
fi

client_name=$1

#useful paths
root="$(cat ./data/rootpath)"
client_root_path=$root/devices/$client_name


#config files
server_config_file="$root/wg0.conf"
server_publickey="$root/devices/server/keys/publickey.pem"
client_config_path="$root/devices/$client_name/wg0.conf"
server_config_file_backup="$root/devices/$client_name/server_wg0.conf"
iprange_path="$root/config/iprange"
dns_path="$root/config/dnsservers"
previousip_path="$root/config/previousip"
remoteip_path="$root/config/remoteip"


#start errors
#if ip range config file not found in config make it
if [ ! -e $iprange_path ]; then
    echo -e "\e[1;31m[-] configure ip range, use ./setup.sh"
    exit 1
fi


#if dns servers config file not found in config make it
if [ ! -e $dns_path ]; then
    echo -e "\e[1;31m[-] configure dns servers, use ./setup.sh"
    exit 1
fi


#if server config file not found in config make it 
if [ ! -e $server_config_file ]; then
    echo -e "\e[1;31m[-] server config file found, use ./setup.sh"
    exit 1
fi
#end errors

#create clients folder
#craete a client root path if not exist
if [ ! -d $client_root_path ]; then
    mkdir $client_root_path
fi

#get the previous ip, if not exist make it and write a one
if [ ! -e $previousip_path ]; then
    echo "1" > $previousip_path
fi


#create the key folder if exist ask if you wanna change it, if not load previous keys
if [ ! -e "$client_root_path/keys" ]; then
    mkdir $client_root_path/keys
    
    get_privatekey=$(wg genkey)
    wg_privatekey="$get_privatekey"
    wg_publickey=$(echo "$wg_privatekey" | wg pubkey)
    
    echo $wg_privatekey > $client_root_path/keys/privatekey.pem
    echo $wg_publickey > $client_root_path/keys/publickey.pem

else
    echo "Do you want to change the keys? (Y/n): "
    read option

    if [ "$option" == "Y" ]; then

        get_privatekey=$(wg genkey)
        wg_privatekey="$get_privatekey"
        wg_publickey=$(echo "$wg_privatekey" | wg pubkey)

        #save server keys
        echo $wg_privatekey > $client_root_path/keys/privatekey.pem
        echo $wg_publickey > $client_root_path/keys/publickey.pem

    else
        wg_privatekey=$(cat $client_root_path/keys/privatekey.pem)
        wg_publickey=$(cat $client_root_path/keys/publickey.pem)
    fi
fi
#end configs files




#save client in server config file
echo -e "\n" >> $server_config_file
echo "#$client_name" >>  $server_config_file
echo "[Peer]" >>  $server_config_file
echo "PublicKey  = $wg_publickey" >> $server_config_file
previp=$(cat "$previousip_path")
finalip=$(( $previp + 1))
range=$(cat $iprange_path)
client_ip="$range.$finalip/32"
echo "AllowedIPs = $client_ip"  >> $server_config_file
echo "$finalip" > $previousip_path


#backup client in server config file
echo "#$client_name" >  $server_config_file_backup
echo "[Peer]" >>  $server_config_file_backup
echo "PublicKey  = $wg_publickey" >> $server_config_file_backup
echo "AllowedIPs = $client_ip"  >> $server_config_file_backup


#create a wgo.conf client
echo "[Interface]" > $client_config_path
echo "Address = $client_ip" >> $client_config_path
echo "PrivateKey = $wg_privatekey" >> $client_config_path
echo "DNS = $(cat $dns_path)" >> $client_config_path
echo -e "\n" >> $client_config_path
echo "[Peer]" >> $client_config_path
echo "PublicKey = $(cat $server_publickey)" >> $client_config_path
echo "AllowedIPs = 0.0.0.0/0" >> $client_config_path
echo "Endpoint = $(cat $remoteip_path):51820" >> $client_config_path


#end
echo -e "\e[1;32m[+] client $client_name added"