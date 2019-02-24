import rpyc
import socket
from rpyc.utils.server import ThreadedServer


class SBMainServer(rpyc.Service):
    def exposed_sum(self,a,b):
        return a+b



if __name__ == "__main__":
    HOST = socket.gethostbyname(socket.gethostname())
    print(HOST)
    s=ThreadedServer(SBMainServer,port=9487,auto_register=False)
    s.start()