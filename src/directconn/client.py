#!/usr/bin/env python3
import os
import sys
import argparse
import rpyc

from threading import Thread

from fuse import FUSE
from fuseFunction import FuseOperation

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Distributed file system client")
    parser.add_argument('-v','--virtual', required=True, help='Virtual mount point')
    parser.add_argument('-r','--real', required=True, help='Physical mount directory')
    parser.add_argument('-p','--port', required=True, help='Main server port number.')
    parser.add_argument('-a', '--addr', required=False, help='(optional) Main server address, default: localhost')
    


    args = parser.parse_args()

    # controller = Controller() # Temply hard code 
    # Connect main server here


    FUSE(FuseOperation(args.real, args.addr, args.port), args.virtual, foreground=True)