import rpyc
import os.path
import random
import hashlib
import pickle

from pathlib import Path

class Directory(object):
    def __init__(self, name):
        self.name = name # directory name
        self.files = [] # files in this directory

class File(object):
    def __init__(self, virtualPath):
        self.nodeAddress = {2510, } # need to hard code node address
        self.vpath = virtualPath
        self.directory = str(Path(virtualPath).parent)
        self.calculate_PhysicalPath(virtualPath)
            
    def calculate_PhysicalPath(self, virtualPath):
        self.rpath = hashlib.md5(virtualPath.encode()).hexdigest()


class MainServerService(rpyc.Service):
    ### move connect node to client? ###
    #class exposed_Node():
    #    def __init__(self, address, port):
    #       self.address = address
    #       self.port = port

    #    def exposed_get_connection(self):
    #        print("hello")
    #        return rpyc.connect(host = self.address, port = self.port)

    class exposed_Master(object):
        def __init__(self, control_dir):
            self.control_dir = control_dir
            self.nodes = {2510, } # hardcode port for subservers
            self.nextServer = None
            self.directories = {}
            self.files = {}
            self.load_commit()
            self.recordDirectory("/") # Root directory
            
        # Get node object by ip address
        def getNode(self, address):
            if(address in self.nodes):
                #return self.nodes[address]
                return address
            
        # Decide server for next file
        #def decideNextServer(self):
        #    for node in self.nodes:
        #        if(node != self.nextServer.address):
        #            self.nextServer = self.nodes[node]
        #            break
         
        # Get file directory from its virtual path
        def getFileDirectory(self, virtualPath):
            return str(Path(virtualPath).parent)
            
        # Get File record from physical path
        def getFileFromReal(self, realPath):
            for f in self.files:
                if(self.files[f].rpath == realPath):
                    return self.files[f]
                    
            return None
            
        # Record new directory
        def recordDirectory(self, dirName):
            if(dirName in self.directories):
                return
            
            self.directories[dirName] = Directory(dirName)
            print(f"Directory {dirName} recorded.")
            
            self.commit()

        # Remove directory from records
        def removeDirectory(self, virtualPath):
            if(virtualPath in self.directories):
                for f in self.directories[virtualPath].files:
                    self.removeFile(f)
                    
                del self.directories[virtualPath]
                    
                print(f"Directory {virtualPath} removed.")
                    
                self.commit()
                    
        # Record a new file
        def recordFile(self, virtualPath):
            fileDirectory = self.getFileDirectory(virtualPath)
            
            #self.decideNextServer() # Decide node to write
            #file = File(virtualPath, self.nextServer)
            
            file = File(virtualPath)
            self.directories[fileDirectory].files.append(virtualPath)
            self.files[virtualPath] = file
            
            self.commit()
            
            print(f"File {virtualPath} recorded on server {self.nextServer.address}.")
            return file
            
        # Remove file and unregister record
        def removeFile(self, virtualPath):
            fileDirectory = self.getFileDirectory(virtualPath)

            self.directories[fileDirectory].files.remove(virtualPath)

            #file = self.files[virtualPath]
            #node = self.nodes[file.nodeAddress]
            #node.getConnection().root.unlink(file.rpath)
            del self.files[virtualPath]

            self.commit()
            print(f"File {virtualPath} removed from server.")

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
        def load_commit(self):
            if(os.path.isfile(self.control_dir) == False):
                return
            data_file = open(self.control_dir, mode='rb')
            (self.directories, self.files) = pickle.load(data_file)
            data_file.close()

        # Save file hiearchy
        def commit(self):
            data_file = open(self.control_dir, mode='wb')
            pickle.dump((self.directories, self.files), data_file)
            data_file.close()


if __name__ == "__main__":
    
    port = 2220
    s = rpyc.utils.server.ThreadedServer(MainService, port=port)
    
    print("IP: localhost")
    print("Port: ", port)
    print("starting main server service...")
    s.start()