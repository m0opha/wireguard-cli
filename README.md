
Este proyecto tiene como objetivo simplificar la configuración y administración de un servidor WireGuard, así como facilitar la creación de clientes. WireGuard es una tecnología VPN de código abierto que proporciona conexiones seguras y eficientes.

## Características

- Automatización de la configuración del servidor WireGuard.
- Creación sencilla de perfiles de clientes.
- Gestión centralizada de la seguridad y la privacidad de la red.
- [Otras características y ventajas del proyecto...]

## Uso

Para comenzar con la configuración del servidor WireGuard y la creación de clientes, ejecuta el siguiente script:

<!--sec data-title="Your first command: OS X and Linux" data-id="OSX_Linux_whoami" data-collapse=true ces-->

    #start
    scripts/setup.sh

    #add client
    scripts/add_client.sh "client-name"

    #delete client
    scripts/del_client.sh "client-name"
    
<!--endsec-->


