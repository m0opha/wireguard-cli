import os
from src.modules.Useful_functions import loadenv

from src.Menus.server_menu import MenuServerSettings
from src.Menus.Client_menu import MenuClientSettings
from src.Menus.show_config_menu import MenuShowConfig

loadenv(".") # "." make reference to root directory of the project

def main():

    while True:
        os.system("clear")
        MenuShowConfig()
        option = input("Server/clients config (s/c/exit) : ")
        if option in ["Server","server","s","S"]:
            MenuServerSettings()
            
        elif option in ["Clients","clients","c","C"]:
            MenuClientSettings()
        else:
            pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass


