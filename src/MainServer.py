import rpyc
import socket
from rpyc.utils.server import ThreadedServer

def set_config():
    config = configparser.ConfigParser()
    config.read('configure.ini')
    block_size = int()



class SBMainServer(rpyc.Service):
    def exposed_sum(self,a,b):
        return a+b



if __name__ == "__main__":
    set_config()

    HOST = socket.gethostbyname(socket.gethostname())
    print(HOST)
    s=ThreadedServer(SBMainServer,port=9487,auto_register=False)
    s.start()