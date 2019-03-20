#!/usr/bin/env python3
import os
import sys
import argparse

from fuse import FUSE
from fuse_for_client import Passthrough
from threading import Thread

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Distributed file system client")
    parser.add_argument('-v','--virtual', required=True, help='Virtual mount point')    
    parser.add_argument('-d','--address', required=False, default='localhost', help='Address for main server')
    parser.add_argument('-p','--port', required=True, help='Port for main server')

    args = parser.parse_args()
    username = input("Username: ") # get username

    # start FUSE, code is in fuse_for_client.py
    FUSE(Passthrough(args.address, args.port, username), \
        args.virtual, foreground=True, allow_other=True)
