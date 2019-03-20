#!/usr/bin/env python3
import uuid
import os
from rpyc.utils.server import ThreadedServer
from subserverService import Subserver

if __name__ == "__main__":
    
    subserver_port = input("Input the port for the Subserver: ")
    sub  = ThreadedServer(Subserver(int(subserver_port)), port = int(subserver_port), protocol_config={ 'allow_public_attrs': True, })

    print("IP: localhost")
    print("Port: ", subserver_port)
    print("Starting sub server service...")

    sub.start()