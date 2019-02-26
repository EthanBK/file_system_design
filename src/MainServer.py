import rpyc
# import socket
# from rpyc.utils.server import ThreadedServer
import configparser
import os
import math
import uuid
import random

def set_config():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    cf = os.path.join(THIS_FOLDER, 'configure.conf')
    config = configparser.ConfigParser()
    config.read(cf)
    MainServerService.block_size = \
        int(config.get('mainServer', 'block_size'))
    MainServerService.replication_factor = \
        int(config.get('mainServer', 'replication_factor'))
    # print(block_size, replication_factor)
    
"""
Main server services
"""
class MainServerService(rpyc.Service):
    def __init__(self):    
        self.block_size = 0             # size of each block
        self.replication_factor = 0     # number of replicates of each block
        self.subserver = {}             # unique id for each subserver
        self.file_table = {}            # 


    """
    Expose main server services to client
    """
    class Exopsed_main():

        def exposed_sum(self,a,b):
            return a+b
    


    # Return the number of block needed for storing file of size <size>
    def get_num_blocks(self, size):
        return int(math.ceil()(float(size) / self.block_size))


    # Return the (block id, subserver id) array of current target.
    def get_block_id(self, target, num_block):
        blocks = []
        for _ in range(num_block):
            # get id for each block
            block_id = uuid.uuid1()
            # get id for target sub server 
            subserv_id = random.sample(self.subserver, num_block)
            # add (block id, subserver id) as a tuple in <blocks>
            tpl = (block_id, subserv_id)
            blocks.append(tpl)
            # add tuple to file table
            # Todo: What is target?
            self.file_table[target].append(tpl)
        return blocks


if __name__ == "__main__":
    set_config()
    port = 2220
    s = rpyc.utils.server.ThreadedServer(MainServerService, port = port)
    
    print("IP: localhost")
    print("Port: ", port)
    print("starting main server service...")
    s.start()
    # HOST = socket.gethostbyname(socket.gethostname())
    # print(HOST)
    # s=ThreadedServer(SBMainServer,port=9487,auto_register=False)
    # s.start()