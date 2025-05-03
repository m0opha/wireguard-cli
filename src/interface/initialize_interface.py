def getInput(prompt, default=None, validate=None, errorMsg="Valor inválido. Intente de nuevo."):
    while True:
        value = input(f"{prompt} [default: {default}]: ") or default
        if validate:
            try:
                return validate(value)
            except Exception:
                print(errorMsg)
        else:
            return value

def initializeInterface():
    import subprocess

    def detectInterfaces():
        interfaces = []
        try:
            output = subprocess.check_output("ip -o link show | awk -F': ' '{print $2}'", shell=True, text=True)
            interfaces = [i for i in output.strip().split('\n') if i != 'lo']
        except Exception as e:
            print(f"Error detectando interfaces: {e}")
        return interfaces

    def chooseInterface(interfaces):
        if len(interfaces) == 1:
            return interfaces[0]
        print("Interfaces de red detectadas:")
        for idx, iface in enumerate(interfaces):
            print(f"{idx}) {iface}")
        index = getInput("Seleccione la interfaz por número", "0", lambda x: interfaces[int(x)], "Selección inválida.")
        return index

    def validateIP(ip):
        import ipaddress
        return str(ipaddress.ip_address(ip))

    def validatePort(port):
        port = int(port)
        if not 0 < port < 65536:
            raise ValueError("Puerto fuera de rango")
        return str(port)

    def validatePeers(n):
        n = int(n)
        if n < 1:
            raise ValueError("Debe ser al menos 1 peer")
        return n

    interfaces = detectInterfaces()
    selected_interface = chooseInterface(interfaces)

    range_ip = getInput("Range IP", "10.0.0.1", validateIP, "IP inválida.")
    remote_ip = getInput("Remote IP or domain", None, lambda x: x if x.strip() else None, "Debe ingresar una IP o dominio.")
    listen_port = getInput("Port", "51820", validatePort, "Puerto inválido.")
    dns_server = getInput("DNS for clients", "1.1.1.1", validateIP, "DNS inválido.")
    peers = getInput("Number of peers to generate", "1", validatePeers, "Número inválido de peers.")

    config = {
        "range_ip": range_ip,
        "listen_port": listen_port,
        "remote_ip": remote_ip,
        "PostUp": f"iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o {selected_interface} -j MASQUERADE",
        "PostDown": f"iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o {selected_interface} -j MASQUERADE",
        "dns": dns_server,
        "peers": peers,
        "interface": selected_interface,
    }

    return config

