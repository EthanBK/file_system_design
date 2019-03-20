#!/usr/bin/env python3
import uuid
import os
from rpyc.utils.server import ThreadedServer
from mainserverService import Mainserver

if __name__ == "__main__":
    
    main_port = input("Input the port for the Mainserver: ")
    sub  = ThreadedServer(Mainserver(), port = int(main_port), protocol_config={ 'allow_public_attrs': True, })

    print("IP: localhost")
    print("Port: ", main_port)
    print("Starting main server service...")

    sub.start()
