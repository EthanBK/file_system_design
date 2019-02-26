import rpyc
# import socket
# from rpyc.utils.server import ThreadedServer
import configparser
import os





def set_config():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    cf = os.path.join(THIS_FOLDER, 'configure.conf')
    config = configparser.ConfigParser()
    config.readfp(open(cf))
    block_size = int(config.get('mainServer', 'block_size'))
    replication_factor = int(config.get('mainServer', 'replication_factor'))
    # print(block_size, replication_factor)


class SBMainServer(rpyc.Service):
    def exposed_sum(self,a,b):
        return a+b



if __name__ == "__main__":
    set_config()

    # HOST = socket.gethostbyname(socket.gethostname())
    # print(HOST)
    # s=ThreadedServer(SBMainServer,port=9487,auto_register=False)
    # s.start()