#!/bin/bash


#necessary directories
root="$(cat ./data/rootpath)"
config_path="$root/config"
devices_path="$root/devices"


#config files paths
server_config_file_backup="$root/devices/server/wg0.conf"
server_root="$root/devices/server"
iprange_path="$root/config/iprange"
dns_path="$root/config/dnsservers"
remoteip_path="$root/config/remoteip"


#script paths
setting_range_ip_path="./python_scripts/SettingRangeIp.py"
setting_dns_path="./python_scripts/SettingDns.py"


#if config path not exite make it
if [ ! -d "$config_path" ]; then
    mkdir $config_path
fi


#if devices path not exite make it
if [ ! -d "$devices_path" ]; then
    mkdir $devices_path
fi


#create the root path of server
if [ ! -d $server_root ]; then
    mkdir $server_root
fi


#setting ip range default 10.0.0
if [ ! -e $iprange_path ]; then
    python3 $setting_range_ip_path $iprange_path
    
else
    read -p  "[+] Do you want to change the range ip? ( Y/enter) : " option

    if [ "$option" == "Y" ]; then
        python3 $setting_range_ip_path $iprange_path
    fi
fi


#Setting the remote ip 
if [ ! -e $remoteip_path ]; then

    read -p "Enter the remote IP of the server: "  remote_ip
    read -p "Do you want to save this $remote_ip ip? (Y/n) : "  option

    if [ "$option" == "Y" ]; then
        echo $remote_ip >> $remoteip_path
    else
        exit 1
    fi
fi


#configure or create dns server
if [ ! -e $dns_path ]; then
    python3 $setting_dns_path $dns_path

else
    read -p "[+] Do you want to change the DNS servers? ( Y/enter) : " option
    if [ "$option" == "Y" ]; then
        python3 $setting_dns_path $dns_path
        

    fi
fi

#load or create keys
if [ ! -e $server_root/keys ]; then
  
    mkdir $server_root/keys

    #generate keys
    get_privatekey=$(wg genkey)
    wg_privatekey="$get_privatekey"
    wg_publickey=$(echo "$wg_privatekey" | wg pubkey)

    #save server keys
    echo $wg_privatekey > $server_root/keys/privatekey.pem
    echo $wg_publickey > $server_root/keys/publickey.pem

else
    echo "Do you want to change the keys? (Y/n): "
    read option

    if [ "$option" == "Y" ]; then

        get_privatekey=$(wg genkey)
        wg_privatekey="$get_privatekey"
        wg_publickey=$(echo "$wg_privatekey" | wg pubkey)

        #save server keys
        echo $wg_privatekey > $server_root/keys/privatekey.pem
        echo $wg_publickey > $server_root/keys/publickey.pem
    else
        wg_privatekey=$(cat $server_root/keys/privatekey.pem)
        wg_publickey=$(cat $server_root/keys/publickey.pem)
    fi
fi


#create wg0.conf file
echo "[Interface]" > $root/wg0.conf
echo "Address = $(cat $iprange_path).1/24" >> $root/wg0.conf
echo "DNS = $(cat $dns_path)" >> $root/wg0.conf
echo "ListenPort = 51820" >> $root/wg0.conf
echo "PrivateKey = $wg_privatekey" >> $root/wg0.conf
echo "PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE0" >> $root/wg0.conf
echo "PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE" >> $root/wg0.conf


#backup wg0.conf file
echo "[Interface]" > $server_config_file_backup
echo "Address = $(cat $iprange_path).1/24" >> $server_config_file_backup
echo "DNS = $(cat $dns_path)" >> $server_config_file_backup
echo "ListenPort = 51820" >> $server_config_file_backup
echo "PrivateKey = $wg_privatekey" >> $server_config_file_backup
echo "PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE0" >> $server_config_file_backup
echo "PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE" >> $server_config_file_backup


echo -e "\e[1;32m[+] Done :D"