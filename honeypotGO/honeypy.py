#Libraries
import argparse
from ssh_honeypot import *


# Parse Arguments

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-a', '--address', type = str, required = True)
    parser.add_argument('-p', '--port', type = int, required = True)
    parser.add_argument('-u', '--username', type = str)
    parser.add_argument('-pw', '--password', type = str)

    parser.add_argument('-s', '--ssh', action = 'store_true')

    args = parser.parse_args()
    
    try:
        if args.ssh:
            print("[-] Running SSH Honeypot...")
            honeypot(args.address, args.port, args.username, args.password)

            if not args.username:
                username = None
            if not args.password:
                password = None
    except:
        print("[-] Exiting HoneyPy...")
