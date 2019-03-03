import rpyc
import uuid
import os
import configparser
from time import sleep
import threading

from rpyc.utils.server import ThreadedServer

ROOT_DIR = "/tmp/subserver/"

# clean temp file


class SubService(rpyc.Service):


    #def on_connect(self, conn):
     #   print("subserver connected")

    #def on_disconnect(self, conn):
     #   print("subserver disconnected")

    class exposed_Subserver():
        def __init__(self, port):
            self.port = port
            self.dir = ROOT_DIR + str(self.port) + '/'
            if not os.path.isdir(self.dir):
                os.mkdir(self.dir)

        def exposed_write(self, block_id, data):
            """write data to the block in subserver"""
            f = open(self.dir + str(block_id), "w")
            f.write(data)

        def exposed_read(self, block_id):
            """Return block content"""
            block_address = self.dir + str(block_id)
            if not os.path.isfile(block_address):
                return None
            fname = open(block_address)
            return fname.read()

        def exposed_delete_file(self, block_id):
            """Remove block with block_id"""
            block_address = self.dir + str(block_id)
            if not os.path.isfile(block_address):
                return "Warning: No such file!"
            os.remove(block_address)
            return 0


if __name__ == "__main__":
    if not os.path.isdir(ROOT_DIR):
        os.mkdir(ROOT_DIR)
    
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
