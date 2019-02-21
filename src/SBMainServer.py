import rpyc
import socket


class SBMainServer(rpyc.Service):
    def exposed_sum(self,a,b):
        return a+b