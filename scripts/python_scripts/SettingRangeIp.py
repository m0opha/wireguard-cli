import sys

def main():

    while True:
        iprange = input("ip range default (10.0.0): ") 
        if iprange == "":
            iprange = "10.0.0"
        else:
            if len(iprange.split(".")) != 3:
                print("[-] ip range not valid")
                continue
            else:
                pass

        confirm  = input("[+] Do you want to change the range ip? ( Y/enter) : ")
        if confirm in ["Yes","yes","y","Y"]:
            with open(sys.argv[1], "w") as file:
                file.write(iprange)
                exit(0)
        else:
            print("[-] gateway ip not configured")
            exit(1)

if __name__ == "__main__":
    main()
