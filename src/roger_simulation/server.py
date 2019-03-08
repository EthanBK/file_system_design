import rpyc
import uuid
import os
from fuse import FUSE

from rpyc.utils.server import ThreadedServer
from serverService import serverService

FILE_DIR = ["/home/roger/Desktop/ECS251/tbmounted/", "/home/roger/Desktop/ECS251/tbmounted2/", "/home/roger/Desktop/ECS251/tbmounted3/"]

if __name__ == "__main__":
    
    subserver_port = input("Input the port for the Subserver: ")
    sub  = ThreadedServer(serverService(FILE_DIR), port = int(subserver_port), protocol_config={ 'allow_public_attrs': True, })

    print("IP: localhost")
    print("Port: ", subserver_port)
    print("Starting sub server service...")

    sub.start()
