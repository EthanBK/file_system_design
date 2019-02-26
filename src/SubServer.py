import rpyc
import uuid
import os

from rpyc.utils.server import ThreaderServer

class SubService(rpyc.Service):
    class exposed_Subserver():
        def expoed_delete_file



        def exposed_write(uuid, data, numSubs):
            f = open(uuid, "x")
            f.write(data)
            if len(numSub) >= 1
                self.storeTo(uuid, data)

        def exposed_storeTo(uuid, data, numSubs):
            host, port = numSub[0]
            numSub = numSub[1:]
            self.write(uuid, data, numSub)
            
            

