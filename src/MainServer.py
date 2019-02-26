import rpyc
# import socket
# from rpyc.utils.server import ThreadedServer
import configparser
import os
import math
import uuid
import random


def set_config():
    cur_folder = os.path.dirname(os.path.abspath(__file__))
    cf = os.path.join(cur_folder, 'configure.conf')
    config = configparser.ConfigParser()
    config.read(cf)
    MainServerService.block_size = \
        int(config.get('mainServer', 'block_size'))
    MainServerService.replication_factor = \
        int(config.get('mainServer', 'replication_factor'))
    # print(block_size, replication_factor)


# Main server service
class MainServerService(rpyc.Service):
    # expose main service to client
    class exposed_MainServer:
        block_size = 0             # size of each block
        replication_factor = 0     # number of replicates of each block
        subserver = {}             # unique id for each subserver
        file_table = {}            # 


        # Create file table entry (empty) for target file based on srouce file size
        # Return:
        #   blocks -> (block id, sub server id) tuple array
        #   
        def exposed_creat_file_table_entry(self, target, src_size):
            if target not in self.__class__.file_table:
                # Create entry for thix file 
                self.__class__.file_table[target] = []
            num_block = self.get_num_blocks(src_size)
            blocks = self.get_blocks(target, num_block)     
            return blocks

        # Return the number of block needed for storing file of size <size>
        def get_num_blocks(self, size):
            return int(math.ceil((float(size) / self.__class__.block_size)))
        
        def exposed_get_block_size(self):
            return self.__class__.block_size

        # Assign a number of block with random sub servers
        # Return the (block id, subserver id) array of current target.
        def get_blocks(self, target, num_block):
            blocks = []
            for _ in range(num_block):
                # get id for each block
                block_id = uuid.uuid1()
                # get id for target sub server 
                subserver_id = random.sample(self.__class__.subserver, num_block)
                # add (block id, sub server id) as a tuple in <blocks>
                tpl = (block_id, subserver_id)
                blocks.append(tpl)
                # add tuple to file table
                # Todo: What is target?
                self.__class__.file_table[target].append(tpl)
            return blocks


if __name__ == "__main__":
    set_config()
    port = 2220
    s = rpyc.utils.server.ThreadedServer(MainServerService, port=port)
    
    print("IP: localhost")
    print("Port: ", port)
    print("starting main server service...")
    s.start()
    # HOST = socket.gethostbyname(socket.gethostname())
    # print(HOST)

