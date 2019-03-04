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

<<<<<<< HEAD
    # todo: advanced function
    k = Thread(target = t)
    k.start()
=======
    # Build connection\
    port = int(args.port)
    con = rpyc.connect("localhost", port = port)
    main_server_service_exposed = con.root.MainServer()
>>>>>>> 94ffb6de0b13b09a2b38c3888d0b9ec68c32af72


<<<<<<< HEAD
    k.join()
=======
    FUSE(Passthrough(), args.virtual, foreground=True)
>>>>>>> 94ffb6de0b13b09a2b38c3888d0b9ec68c32af72
