import rpyc
import uuid
import os
from fuse import FUSE

from rpyc.utils.server import ThreadedServer
from subserver_service import subService


#FILE_DIR = "/home/roger/Desktop/ECS251/tbmounted/"

if __name__ == "__main__":
    
    subserver_port = input("Input the port for the Subserver: ")
    sub  = ThreadedServer(subService, port = int(subserver_port), protocol_config={ 'allow_public_attrs': True, })



    print("IP: localhost")
    print("Port: ", subserver_port)
    print("Starting sub server service...")

    sub.start()
