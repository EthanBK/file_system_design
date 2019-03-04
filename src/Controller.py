import rpyc
import os.path
import random

from pathlib import Path

class Subserver():
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.active = False


    def get_connection(self):
        self.con = rpyc.connect(host=self.addr, port=self.port)
        return self.con

    def close_connection(self):
        self.active = False
        self.con.close()


class Directory():
    def __init__(self, name):
        self.name = name    # Dict name
        self.files = []     # v_path of the file in this dict


class File():
    def __init__(self, v_path, subser):
        self.subser = subser
        self.v_path = v_path
        self.dir = str(Path(v_path).parent)

    def get_real_Path(self, v_path):
        pass


class Controller:
    def __init__(self):
        self.subserver = {}     # {port: subser_obj}
        self.directory = {}    # {dir_name: }
        self.file_table = {}    # {v_path: file_obj}

    def generateSubser(self, host):
        addr, port = host
        subser = Subserver(addr, port)
        self.subserver[port] = subser

    # Get next subserver to write, current only on random basis
    # Future: based on the storage of each subserver
    def get_next_subserver(self):
        return random.choice(self.subserver.values())

    def get_subserver(self, port):
        if port in self.subserver:
            return self.subserver[port]
        else:
            print("Error: No subserver found in give port!")
            
    def create_dictionary(self, dir_name):
        if dir_name in self.directory:
            return 
        else:
            self.directory[dir_name] = Directory(dir_name)

    def get_file_dic(self, v_path: "Virtual Path (path on client side)"):
        return str(Path(v_path).parent)

    def createFile(self, v_path: "Virtual Path (path on client side)"):
        file_dic = self.get_file_dic(v_path)
        subser = self.get_next_subserver()
        file_entry = File(v_path, subser)
        self.file_table[v_path] = file_entry
        self.directory[file_dic].files.append(v_path)