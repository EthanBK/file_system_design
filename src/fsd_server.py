import socket
from rpyc.utils.server import ThreadedServer
from SBMainServer import SBMainServer

if __name__ == "__main__":
    print("Starting server on " + socket.gethostname() + "...")
    s=ThreadedServer(SBMainServer,port=2222,auto_register=False)
    s.start()
