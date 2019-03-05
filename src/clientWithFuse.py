import os
import sys
import argparse
import rpyc

<<<<<<< HEAD

from fuse import FUSE
from fuseFunction import Passthrough
from MainServer import 

=======
>>>>>>> c6e213d263ff367639865d79d8bc1ce260c2401c
from threading import Thread

from fuse import FUSE
from fuseFunction import FuseOperation
from Controller import Controller

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Distributed file system client")
    parser.add_argument('-v','--virtual', required=True, help='Virtual mount point')
    parser.add_argument('-r','--real', required=True, help='Physical mount directory')
    parser.add_argument('-p','--port', required=True, help='Port for main server endpoint')

    args = parser.parse_args()

    # todo: advanced function
<<<<<<< HEAD
    k = Thread(target = t)
    k.start()


    k.join()
=======
    # k = Thread(target)
    # k.start()
    # Build connection\
    # port = int(args.port)
    # con = rpyc.connect("localhost", port = port)
    # main_server_service_exposed = con.root.MainServer()

    # subserver = main_server_service_exposed.get_subserver_list()
    # print(subserver)
    # k.join()
    controller = Controller()

    FUSE(FuseOperation(args.real, controller), args.virtual, foreground=True)
>>>>>>> c6e213d263ff367639865d79d8bc1ce260c2401c
