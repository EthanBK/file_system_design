import os
import sys
import argparse


from fuse import FUSE
from fuse_for_client import Passthrough

from threading import Thread



#def main(mountpoint, root):
#    FUSE(Passthrough(root), mountpoint, nothreads=True, foreground=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Distributed file system client")
    parser.add_argument('-v','--virtual', required=True, help='Virtual mount point')
    parser.add_argument('-p','--port', required=True, help='Port for server endpoint')
    #parser.add_argument('-r','--real', required=True, help='Physical mount directory')
    #-parser.add_argument('--hosts', required=True,nargs='+', help='List of hosts')

    args = parser.parse_args()
    FUSE(Passthrough(args.port), args.virtual, foreground=True, allow_root=True)
