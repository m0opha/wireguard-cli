import sys

def main():
    dnsservers = input("add dns server, default ( 8.8.8.8, 8.8.4.4 ) : ")

    if dnsservers != "":
        with open(sys.argv[1],"w") as file:
            file.write(dnsservers)
    else:
         with open(sys.argv[1],"w") as file:
            file.write("8.8.8.8, 8.8.4.4")


if __name__ == "__main__":
    main()
