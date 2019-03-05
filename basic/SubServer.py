import rpyc
import uuid
import os

from rpyc.utils.server import ThreadedServer

FILE_DIR = "/tmp/subserver/"

class SubService(rpyc.Service):

    #def on_connect(self, conn):
     #   print("subserver connected")

    #def on_disconnect(self, conn):
     #   print("subserver disconnected")

    class exposed_Subserver():

        def exposed_write(self, block_id, data):
            """write data to the block in each subserver"""
            f = open(FILE_DIR + str(block_id), "w")
            f.write(data)

        def exposed_read(self, block_id):
            """Return block content"""
            block_address = FILE_DIR + str(block_id)
            if not os.path.isfile(block_address):
                return None
            fname = open(block_address)
            return fname.read()

        def exposed_delete_file(self, block_id):
            """Remove block with block_id"""
            block_address = FILE_DIR + str(block_id)
            if not os.path.isfile(block_address):
                return None
            os.remove(block_address)
            return True

if __name__ == "__main__":
    if not os.path.isdir(FILE_DIR):
        os.mkdir(FILE_DIR)
        
    subserver_port = input("Input the port for the Subserver: ")
    sub  = ThreadedServer(SubService(), port = int(subserver_port))

    print("IP: localhost")
    print("Port: ", subserver_port)
    print("Starting sub server service...")
    sub.start()
