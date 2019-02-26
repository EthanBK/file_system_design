import rpyc
import uuid
import os

from rpyc.utils.server import ThreadedServer

class SubService(rpyc.Service):
    class exposed_Subserver():
        def exposed_delete_file(self, 
