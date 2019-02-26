import rpyc
import uuid
import os

from rpyc.utils.server import ThreaderServer

FILE_DIR = "/tmp/subserver/"

class SubService(rpyc.Service):
    class exposed_Subserver():
        chunks = {}

        def exposed_delete_file(self, block_id):
            """Remove block with block_id"""
            block_address = FILE_DIR + str(block_id)
            if not os.path.isfile(block_address):
                return None
            os.remove(block_address)
            return True
