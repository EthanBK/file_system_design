import uuid
import os
from rpyc.utils.server import ThreadedServer
from serverService import serverService

#FILE_DIR = ["/home/roger/Desktop/ECS251/tbmounted/"]
FILE_DIR = ["/home/pearlhsu/Documents/subserver1/", "/home/pearlhsu/Documents/subserver2/", "/home/pearlhsu/Documents/subserver3/"]


if __name__ == "__main__":
    
    subserver_port = input("Input the port for the Subserver: ")
    sub  = ThreadedServer(serverService(FILE_DIR), port = int(subserver_port), protocol_config={ 'allow_public_attrs': True, })

    print("IP: localhost")
    print("Port: ", subserver_port)
    print("Starting sub server service...")

    sub.start()
