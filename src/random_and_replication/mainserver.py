import rpyc
# import socket
# from rpyc.utils.server import ThreadedServer
import configparser
import os
import math
import uuid
import random

# Main server service
class MainServerService(rpyc.Service):
    def __init__(self):
        self.block_size = 10             # size of each block
        self.split_num = 3    # each file is splitted into {split_num} blocks
        self.replication_factor = 2     # number of replicates of each block
        self.subserver = {2510: ('localhost', 2510), 2511:('localhost', 2511)}             # unique id for each subserver
        self.file_table = {}            # {file_name: [(block_id, subserver_ids)]} dictionary

    def exposed_write_determine(self, v_path): # GOOD
        return self.get_blocks_table(v_path)  # return [(block_path, (subserver_ids)), (block_path, (subserver_ids)), ...]


    # Return file table entry corresponding to <v_path>
    def exposed_get_file_table(self, v_path): # GOOD
        if v_path in self.file_table:
            return self.file_table[v_path]
        return None

    def exposed_get_splitNum(self): # GOOD
        return self.split_num

    def exposed_get_sub_server(self, ids):
        return [self.subserver[_] for _ in ids]

    # Assign a number of block with random sub servers
    # Return the (block id, subserver id) array of current target.
    def get_blocks_table(self, v_path): # GOOD
        block_table = []
        self.file_table[v_path] = []
        for b in range(0, self.split_num):
            # get v_path for each block
            block_path = v_path + str(uuid.uuid1())

            # get id for target sub server
            # subserver_ids = (2510, 2511)
            subserver_ids = random.sample(self.subserver.keys(), self.replication_factor)
            
            # add (block path, sub server id) as a tuple in <blocks>
            tpl = (block_path, subserver_ids)
            block_table.append(tpl)

            # add tuple to file table
            self.file_table[v_path].append(tpl)
            print(self.file_table)
        return block_table


if __name__ == "__main__":
    port = 2220
    s = rpyc.utils.server.ThreadedServer(MainServerService, port=port)
    
    print("IP: localhost")
    print("Port: ", port)
    print("starting main server service...")
    s.start()
    # HOST = socket.gethostbyname(socket.gethostname())
    # print(HOST)