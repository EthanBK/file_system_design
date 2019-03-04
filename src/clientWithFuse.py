import os
import sys
import argparse
import rpyc


from fuse import FUSE
from fuseFunction import Passthrough
from MainServer import 

from threading import Thread


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Distributed file system client")
    parser.add_argument('-v','--virtual', required=True, help='Virtual mount point')
    parser.add_argument('-r','--real', required=True, help='Physical mount directory')
    parser.add_argument('-p','--port', required=True, help='Port for main server endpoint')

    args = parser.parse_args()

    # Build connection\
    port = int(args.port)
    con = rpyc.connect("localhost", port = port)
    main_server_service_exposed = con.root.MainServer()


    FUSE(Passthrough(), args.virtual, foreground=True)
