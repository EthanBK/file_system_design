#!/usr/bin/env python3
import rpyc
import math
import random

from fuse import FUSE, FuseOSError, Operations

class Passthrough(Operations):
    def __init__(self, port):
        self.main_ser = ('localhost', 2220)
        self.sub_lis = {2510: ('localhost', 2510), 2511: ('localhost', 2511), 2512: ('localhost', 2512)}
        #self.base_server = random.sample(self.sub_ser.keys(), 1)[0]
        self.return_value = {} # {returnValue of base_server: [(serverID, returnValue), ...]}
        self.duplicate_num = 2
        self.sub_ser = self.select_sub()
        
    def select_sub(self):
        return random.sample(self.sub_lis.keys(), self.duplicate_num)

    def connect_sub(self, sub_id):
        try:
            sub_addr, sub_port = self.sub_lis[sub_id]
            return rpyc.connect(sub_addr, sub_port).root
        except:
            del self.sub_ser[sub_id]
            return None

    ######################
    # Filesystem methods #
    ######################

    def access(self, path, mode):
        for subserver_id in self.sub_ser:
            try:
                returnValue = self.connect_sub(subserver_id).access(path,mode)
            except:
                continue
            return returnValue

    def chmod(self, path, mode):
        for subserver_id in self.sub_ser:
            try:
                returnValue = self.connect_sub(subserver_id).chmod(path,mode)
            except:
                continue
            return returnValue

    def chown(self, path, uid, gid):
        for subserver_id in self.sub_ser:
            try:
                returnValue = self.connect_sub(subserver_id).chown(path,uid,gid)
            except:
                continue
        return returnValue

    def getattr(self, path, fh=None):
        for subserver_id in self.sub_ser:
            try:
                returnValue = self.connect_sub(subserver_id).getattr(path,fh)
            except:
                #print(subserver_id)
                returnValue = self.connect_sub(subserver_id).getattr(path,fh)
                if not returnValue:
                    break
                #print(returnValue)
                continue
        return returnValue

    def readdir(self, path, fh):
        for subserver_id in self.sub_ser:
            try:
                returnValue = self.connect_sub(subserver_id).readdir(path,fh)
            except:
                continue
        return returnValue

    def readlink(self, path):
        for subserver_id in self.sub_ser:
            try:
                returnValue = self.connect_sub(subserver_id).readlink(path)
            except:
                continue
        return returnValue

    def mknod(self, path, mode, dev):
        for subserver_id in self.sub_ser:
            try:
                returnValue = self.connect_sub(subserver_id).mknod(path,mode,dev)
            except:
                continue
        return returnValue

    def rmdir(self, path):
        for subserver_id in self.sub_ser:
            try:
                returnValue = self.connect_sub(subserver_id).rmdir(path)
            except:
                continue
        return returnValue

    def mkdir(self, path, mode):
        for subserver_id in self.sub_ser:
            try:
                returnValue = self.connect_sub(subserver_id).mkdir(path,mode)
            except:
                continue
        return returnValue

    def statfs(self, path):
        for subserver_id in self.sub_ser:
            try:
                returnValue = self.connect_sub(subserver_id).statfs(path)
            except:
                continue
        return returnValue


    def unlink(self, path):
        for subserver_id in self.sub_ser:
            try:
                returnValue = self.connect_sub(subserver_id).unlink(path)
            except:
                continue
        return returnValue

    def symlink(self, name, target):
        for subserver_id in self.sub_ser:
            try:
                returnValue = self.connect_sub(subserver_id).symlink(name,target)
            except:
                continue
        return returnValue

    def rename(self, old, new):
        for subserver_id in self.sub_ser:
            try:
                returnValue = self.connect_sub(subserver_id).rename(old,new)
            except:
                continue
        return returnValue

    def link(self, target, name):
        for subserver_id in self.sub_ser:
            try:
                returnValue = self.connect_sub(subserver_id).link(target,name)
            except:
                continue
        return returnValue

    def utimens(self, path, times=None):
        for subserver_id in self.sub_ser:
            try:
                returnValue = self.connect_sub(subserver_id).utimens(path,times)
            except:
                continue
        return returnValue

    ################
    # File methods #
    ################

    def open(self, path, flags):
        #full_path = self._full_path(path)
        return_list = []
        #subserver_lis = self.pick_subserver()
        for subserver in self.sub_ser:
            try:
                return_list.append((subserver, self.connect_sub(subserver).open(path, flags)))
            except:
                continue        
        self.return_value[path] = return_list
        return return_list[0][1]

    def create(self, path, mode, fi=None):
        print("path: ", path)
        return_list = []
        #subserver_lis = self.pick_subserver()
        for subserver in self.sub_ser:
            try:
                return_list.append((subserver, self.connect_sub(subserver).create(path, mode, fi)))
            except:
                continue
        self.return_value[path] = return_list
        return return_list[0][1]

    def read(self, path, length, offset, fh):
        for subserver, fhandle in self.return_value[path]:
            try:
                return self.connect_sub(subserver).read(path,length,offset,fhandle)
            except:
                continue

    def write(self, path, buf, offset, fh):
        return_bytes = 0
        for subserver, sub_fh in self.return_value[path]:
            try:
                return_bytes = self.connect_sub(subserver).write(path, buf, offset, sub_fh)
            except:
                continue
        return return_bytes

    def truncate(self, path, length, fh=None):
        return_bytes = 0
        for subserver, sub_fh in self.return_value[path]:
            try:
                return_bytes = self.connect_sub(subserver).truncate(path, length, sub_fh)
            except:
                continue
        return return_bytes

    def flush(self, path, fh):
        return_bytes = 0
        for subserver, sub_fh in self.return_value[path]:
            try:
                return_bytes = self.connect_sub(subserver).flush(path, sub_fh)
            except:
                continue
        return return_bytes

    def release(self, path, fh):
        return_bytes = 0
        for subserver, sub_fh in self.return_value[path]:
            try:
                return_bytes = self.connect_sub(subserver).release(path, sub_fh)
            except:
                continue
        return return_bytes

    def fsync(self, path, fdatasync, fh):
        return_bytes = 0
        for subserver, sub_fh in self.return_value[path]:
            try:
                return_bytes = self.connect_sub(subserver).fsync(path, fdatasync, sub_fh)
            except:
                continue
        return return_bytes