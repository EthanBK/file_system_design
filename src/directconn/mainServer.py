#!/usr/bin/env python3
import rpyc
import os.path
import random
import hashlib
import pickle
import configparser

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

class MainServerService(rpyc.Service):
    class exposed_Mainserver(object):
        class exposed_Directory(object):
            def __init__(self, name):
                self.exposed_name = name    # Dict name
                self.exposed_files = []     # v_path of the file in this dict

        class exposed_File(object):
            def __init__(self, v_path, subser_addr):
                self.subser_addr = subser_addr    # subserver address where this file located
                self.v_path = v_path
                self.dir = str(Path(v_path).parent)
                self.r_path = self.get_real_Path(v_path)

            def get_real_Path(self, v_path):
                return v_path.hashlib.md5(v_path.encode()).hexdigest()

        def __init__(self, config_pkg):
            # config_pkg un-packing
            [self.block_size,
             self.replication_factor,
             self.main_server_port,
             self.num_subserver,
             self.subser,
             self.sub_server_root_dir] = config_pkg

            # Container Definition
            self.exposed_subservers = {}     # {port (address in later work): (subserver_ip, subserver_port))}
            self.exposed_directories = {}    # {v_path: Dir_obj}
            self.exposed_file_table = {}    # {v_path: file_obj}

            # Build obj for subserver
            for i in range(len(self.subser)):
                self.exposed_generate_subser(self.subser[i][0], self.subser[i][1])

        def exposed_print_one(self):
            return 1
            
        def exposed_generate_subser(self, addr, port):
            subser = Subserver(addr, port)
            self.exposed_subservers[port] = subser

        # Get next subserver to write, current only on random basis
        # Future: based on the storage of each subserver
        def exposed_get_next_subserver(self):
            return random.choice(self.exposed_subservers.values())

        # Given the virtual path, find which subserver is storing it.
        def exposed_find_subserver(self, v_path):
            try:
                return self.exposed_file_table[v_path].subser
            except:
                print("Error: path is not file system!")

        # port ==> obj subserver
        def exposed_get_subserver(self, port):
            if port in self.exposed_subservers:
                return self.exposed_subservers[port]
            else:
                print("Error: No subserver found in give port!")
            
        def exposed_create_dictionary(self, v_path):
            if(v_path in self.exposed_directories):
                return
            else:
                self.exposed_directories[v_path] = self.exposed_Directory(v_path)
                
        # Remove directory from records
        # todo: what about dir inside this dir
        def exposed_remove_directory(self, v_path):
            if(v_path in self.exposed_directories):
                for f in self.exposed_directories[v_path].files:
                    self.exposed_remove_file(f)
                del self.exposed_directories[v_path]
                print(f"Directory {v_path} removed.")
        print("Warning: Directory does not exist!")
    #    self.commit()
        
        def exposed_get_file_dir(self, v_path):
            return str(Path(v_path).parent)
        
        def exposed_create_file(self, v_path):
            file_dir = self.exposed_get_file_dir(v_path)
            subser = self.exposed_get_next_subserver()
            file_entry = self.exposed_File(v_path, subser)
            self.exposed_file_table[v_path] = file_entry
            self.exposed_directories[file_dir].files.append(v_path)
            print(f"<create_file>: File {v_path} created on the server {subser}.")
            return file_entry
            
        def exposed_remove_file(self, v_path):
            file_dir = self.exposed_get_file_dir(v_path)
            self.exposed_directories[file_dir].files.remove(v_path)

            del self.exposed_file_table[v_path]
            print(f"<remove_file>: File {v_path} removed from server.")
        
        # Get File record from physical path
        def exposed_file_fromReal(self, realPath):
            for f in self.exposed_file_table.keys():
                if(self.exposed_file_table[f].r_path == realPath):
                    return self.exposed_file_table[f]
            return None

    # Save file hiearchy
    #def commit(self):
    #    data_file = open(self.control_dir, mode='wb')
    #    pickle.dump((self.exposed_directories, self.exposed_file_table), data_file)
    #    data_file.close()

    # Node migration
    #def migrate(self,host):
        # Select new host
    #    newHost = host
    
    #    for node in self.nodes:
    #        if(host != node):
    #           newHost = node
    #            break

    #    if(newHost == host):
    #        print("No eligible hosts found for migration.")
    #        return
    
    #    print(f"Migrating from {host} to  {newHost}")

        # Send new host ip
    #    self.nodes[host].getConnection().root.migrate(newHost)
    
    #    for f in self.files:
    #        fileRecord = self.files[f]
    #        if(fileRecord.nodeAddress == host):
    #            fileRecord.nodeAddress = newHost
            
    #    self.nodes[host].shutdown()
    #    del self.nodes[host]
    #    print("Migration completed")

    # Load file hiearchy from backup
    # def load_commit(self):
    #     if(os.path.isfile(self.control_dir) == False):
    #         return
    #     data_file = open(self.control_dir, mode='rb')
    #     (self.exposed_directories, self.files) = pickle.load(data_file)
    #     data_file.close()

    