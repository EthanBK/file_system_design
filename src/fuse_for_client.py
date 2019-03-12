#!/usr/bin/env python
import rpyc

from fuse import FUSE, FuseOSError, Operations

class Passthrough(Operations):
    def __init__(self, addr, port, user_info):
        self.addr = addr
        self.port = port
        self.user_info = user_info
        rpyc.connect(self.addr, self.port).root.get_user_info(user_info)


    ######################
    # Filesystem methods #
    ######################

    def access(self, path, mode):
        return rpyc.connect(self.addr, self.port).root.access(path,mode,self.user_info)

    def chmod(self, path, mode):
        return rpyc.connect(self.addr, self.port).root.chmod(path,mode,self.user_info)

    def chown(self, path, uid, gid):
        return rpyc.connect(self.addr, self.port).root.chown(path,uid,gid,self.user_info)

    def getattr(self, path, fh=None):
        return rpyc.connect(self.addr, self.port).root.getattr(path,self.user_info,fh)

    def readdir(self, path, fh):
        return rpyc.connect(self.addr, self.port).root.readdir(path,fh,self.user_info)

    def readlink(self, path):
        return rpyc.connect(self.addr, self.port).root.readlink(path,self.user_info)

    def mknod(self, path, mode, dev):
        return rpyc.connect(self.addr, self.port).root.mknod(path,mode,dev,self.user_info)

    def rmdir(self, path):
        return rpyc.connect(self.addr, self.port).root.rmdir(path,self.user_info)

    def mkdir(self, path, mode):
        return rpyc.connect(self.addr, self.port).root.mkdir(path,mode,self.user_info)

    def statfs(self, path):
        return rpyc.connect(self.addr, self.port).root.statfs(path,self.user_info)

    def unlink(self, path):
        return rpyc.connect(self.addr, self.port).root.unlink(path,self.user_info)

    def symlink(self, name, target):
        return rpyc.connect(self.addr, self.port).root.symlink(name,target,self.user_info)

    def rename(self, old, new):
        return rpyc.connect(self.addr, self.port).root.rename(old,new,self.user_info)

    def link(self, target, name):
        return rpyc.connect(self.addr, self.port).root.link(target,name,self.user_info)

    def utimens(self, path, times=None):
        return rpyc.connect(self.addr, self.port).root.utimens(path,self.user_info,times)


    ################
    # File methods #
    ################

    def open(self, path, flags):
        return rpyc.connect(self.addr, self.port).root.open(path,flags,self.user_info)

    def create(self, path, mode, fi=None):
        print("path: ", path)
        return rpyc.connect(self.addr, self.port).root.create(path,mode,self.user_info,fi)

    def read(self, path, length, offset, fh):
        return rpyc.connect(self.addr, self.port).root.read(path,length,offset,fh,self.user_info)

    def write(self, path, buf, offset, fh):
        return rpyc.connect(self.addr, self.port).root.write(path,buf,offset,fh,self.user_info)

    def truncate(self, path, length, fh=None):
        return rpyc.connect(self.addr, self.port).root.truncate(path,length,self.user_info,fh)

    def flush(self, path, fh):
        return rpyc.connect(self.addr, self.port).root.flush(path,fh,self.user_info)

    def release(self, path, fh):
        return rpyc.connect(self.addr, self.port).root.release(path,fh,self.user_info)

    def fsync(self, path, fdatasync, fh):
        return rpyc.connect(self.addr, self.port).root.fsync(path,fdatasync,fh,self.user_info)

