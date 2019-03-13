import os
import sys
import argparse

from fuse import FUSE
from fuse_for_client import Passthrough

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Distributed file system client")
    parser.add_argument('-v','--virtual', required=True, help='Virtual mount point')    
    parser.add_argument('-d','--address', required=False, default='localhost', help='Address for server')
    parser.add_argument('-p','--port', required=True, help='Port for server endpoint')

    args = parser.parse_args()
    username = input("Username: ")
    #password = input("Password: ")
    #user_info = username + "_" +password
    user_info = username
    FUSE(Passthrough(args.address, args.port, user_info), \
        args.virtual, foreground=True, allow_other=True)
