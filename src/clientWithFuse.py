import os
import sys
import argparse
import rpyc


from fuse import FUSE
from fuseFunction import Passthrough

from threading import Thread

def t(controller):
    while(True):
        if(i[0:8] == "shutdown"):
            host = str(i).split('-')[1]
        elif(i == "q"):
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Distributed file system client")
    parser.add_argument('-v','--virtual', required=True, help='Virtual mount point')
    parser.add_argument('-r','--real', required=True, help='Physical mount directory')
    #parser.add_argument('-p','--port', required=True, help='Port for server endpoint')
    #parser.add_argument('--hosts', required=True,nargs='+', help='List of hosts')
    parser.add_argument('--clear', required=False,type=int, help='Clear control backup file')

    args = parser.parse_args()
    
    if(args.clear == 1):
        # Remove control layer data
        try:
            os.remove(args.control)
        except:
            pass


    k = Thread(target = t)
    k.start()

    FUSE(Passthrough(args.real), args.virtual, foreground=True)
    
    k.join()
