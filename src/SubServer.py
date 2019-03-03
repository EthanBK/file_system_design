import rpyc
import uuid
import os
import configparser
from time import sleep
import threading

from MainServer import set_config
from rpyc.utils.server import ThreadedServer

FILE_DIR = "/tmp/subserver/"

class SubService(rpyc.Service):

    #def on_connect(self, conn):
     #   print("subserver connected")

    #def on_disconnect(self, conn):
     #   print("subserver disconnected")

    class exposed_Subserver():

        def exposed_write(self, block_id, data):
            """write data to the block in subserver"""
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
    
    cur_folder = os.path.dirname(os.path.abspath(__file__))
    cf = os.path.join(cur_folder, 'configure.conf')
    parser = configparser.ConfigParser()
    parser.read(cf)
    subservers = \
        [int(v.strip()) for v in parser.get('subServer', 'port').split(',')]
    
    def start_subserver():
        port = subservers[i]
        print("Initilizing Subserver", i)
        print("IP: localhost")
        print("Port: ", port)
        sub  = ThreadedServer(SubService(), port=port)
        sub.start()

    for i in range(len(subservers)):
        print(i)
        thread = threading.Thread(target=start_subserver)
        thread.start()
        sleep(1)
