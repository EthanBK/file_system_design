import rpyc
import uuid
import os

from rpyc.utils.server import ThreaderServer

class SubService(rpyc.Service):
    class exposed_Subserver():
        def expoed_delete_file
