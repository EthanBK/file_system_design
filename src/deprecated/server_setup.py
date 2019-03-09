"""
This script initialize mainserver and all subservers.


"""
import os
import rpyc 
import configparser
import threading 
import socket

from time import sleep
from rpyc.utils.server import ThreadedServer
from SubServerService import SubServerService
from mainServer import MainServerService

block_size = float('inf')
relication_factor = 1
main_server_port = 0
num_subserver = 0
subservers  = []
sub_server_root_dir = []

def set_config():
    cur_folder = os.path.dirname(os.path.abspath(__file__))
    cf = os.path.join(cur_folder, 'configure.conf')
    parser = configparser.ConfigParser()
    parser.read(cf)
    # Read parameters
    block_size = \
        int(parser.get('mainServer', 'block_size'))
    replication_factor = \
        int(parser.get('mainServer', 'replication_factor'))
    main_server_port = \
        int(parser.get('mainServer', 'port'))
    num_subserver = \
        int(parser.get('subServer', 'num_subserver'))
    subserver_port = \
        [int(v.strip()) for v in parser.get('subServer', 'port').split(',')]
    subserver_addr = \
        [v.strip() for v in parser.get('subServer', 'addr').split(',')]
    sub_server_root_dir = \
        parser.get('subServer', 'ROOT_DIR')
    # print(subserver_addr)
    # print(subserver_port)
    # print(list(zip(subserver_addr, subserver_port)))

    return [block_size,
            replication_factor,
            main_server_port,
            num_subserver,
            list(zip(subserver_addr, subserver_port)),
            sub_server_root_dir]

def start_subserver(addr, port):
    print(f"Starting subserver {port} on {addr}...\n")
    subss  = ThreadedServer(SubServerService(port, sub_server_root_dir), 
                            port=port)
    subss.start()

def start_main_server(addr, port, config_pkg):
    print(f"Starting central server {port} on {addr}...\n")
    mss = ThreadedServer(MainServerService(config_pkg), 
                        port=port, protocol_config={ 'allow_public_attrs': True, })
    mss.start()


if __name__ == "__main__":
    
    # Load configuration
    config_pkg = set_config()

    [block_size,
    replication_factor,
    main_server_port,
    num_subserver,
    subservers,     # (addr, port) tuple
    sub_server_root_dir] = config_pkg

    host_name = socket.gethostname()
    host_addr = socket.gethostbyname(host_name)
    # Start Main server (controller)
    thread = threading.Thread(target=start_main_server, args=(host_addr, main_server_port, config_pkg))
    thread.start()
    sleep(1)

    # Start subserver 
    # Create root dir for sub server
    if not os.path.isdir(sub_server_root_dir):
        os.mkdir(sub_server_root_dir)
    for i in range(len(subservers)):
        port = subservers[i][1]
        print(f"Starting subserver... ({i+1}/{num_subserver})\n")
        thread = threading.Thread(target=start_subserver, args=(host_addr, port))
        thread.start()
        sleep(1)

    