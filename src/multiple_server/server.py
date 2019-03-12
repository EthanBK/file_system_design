import uuid
import os
from rpyc.utils.server import ThreadedServer
from serverService import serverService

#FILE_DIR = ["/home/zzc558/Documents/tbmounted001/"]
#FILE_DIR = ["/home/roger/Desktop/ECS251/tbmounted/", "/home/roger/Desktop/ECS251/tbmounted2/", "/home/roger/Desktop/ECS251/tbmounted3/"]
FILE_DIR = "/tmp/subserver/"


if __name__ == "__main__":
    
    subserver_port = input("Input the port for the Subserver: ")
    sub  = ThreadedServer(serverService(FILE_DIR, int(subserver_port)), port = int(subserver_port), protocol_config={ 'allow_public_attrs': True, })

    print("IP: localhost")
    print("Port: ", subserver_port)
    print("Starting sub server service...")

    sub.start()
