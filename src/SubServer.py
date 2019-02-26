import rpyc
import uuid
import os

from rpyc.utils.server import ThreaderServer

FILE_DIR = "/tmp/subserver/"

class SubService(rpyc.Service):
    class exposed_Subserver():
<<<<<<< HEAD
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
            
            

=======
        chunks = {}

        def exposed_delete_file(self, block_id):
            """Remove block with block_id"""
            block_address = FILE_DIR + str(block_id)
            if not os.path.isfile(block_address):
                return None
            os.remove(block_address)
            return True
>>>>>>> 4b6cbc4bc368e528291f11012794d70b3c51958e
