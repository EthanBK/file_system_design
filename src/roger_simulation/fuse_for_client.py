#!/usr/bin/env python
import rpyc

from fuse import FUSE, FuseOSError, Operations

class Passthrough(Operations):
    def __init__(self, port):
        self.port = port
        #self.subserverRootDir = rpyc.connect('localhost',port).root.getRoot


    ######################
    # Filesystem methods #
    ######################

    def access(self, path, mode):
        return rpyc.connect('localhost', self.port).root.access(path,mode)

    def chmod(self, path, mode):
        return rpyc.connect('localhost', self.port).root.chmod(path,mode)

    def chown(self, path, uid, gid):
        return rpyc.connect('localhost', self.port).root.chown(path,uid,gid)

    def getattr(self, path, fh=None):
        return rpyc.connect('localhost', self.port).root.getattr(path,fh)

    def readdir(self, path, fh):
        return rpyc.connect('localhost', self.port).root.readdir(path,fh)

    def readlink(self, path):
        return rpyc.connect('localhost', self.port).root.readlink(path)

    def mknod(self, path, mode, dev):
        return rpyc.connect('localhost', self.port).root.mknod(path,mode,dev)

    def rmdir(self, path):
        return rpyc.connect('localhost', self.port).root.rmdir(path)

    def mkdir(self, path, mode):
        return rpyc.connect('localhost', self.port).root.mkdir(path,mode)

    def statfs(self, path):
        return rpyc.connect('localhost', self.port).root.statfs(path)

    def unlink(self, path):
        return rpyc.connect('localhost', self.port).root.unlink(path)

    def symlink(self, name, target):
        return rpyc.connect('localhost', self.port).root.symlink(name,target)

    def rename(self, old, new):
        return rpyc.connect('localhost', self.port).root.rename(old,new)

    def link(self, target, name):
        return rpyc.connect('localhost', self.port).root.link(target,name)

    def utimens(self, path, times=None):
        return rpyc.connect('localhost', self.port).root.utimens(path,times)


    ################
    # File methods #
    ################

    def open(self, path, flags):
        #full_path = self._full_path(path)
        return rpyc.connect('localhost', self.port).root.open(path,flags)

    def create(self, path, mode, fi=None):
        print("path: ", path)
        return rpyc.connect('localhost', self.port).root.create(path,mode,fi)

    def read(self, path, length, offset, fh):
        return rpyc.connect('localhost', self.port).root.read(path,length,offset,fh)

    def write(self, path, buf, offset, fh):
        return rpyc.connect('localhost', self.port).root.write(path,buf,offset,fh)

    def truncate(self, path, length, fh=None):
        return rpyc.connect('localhost', self.port).root.truncate(path,length,fh)

    def flush(self, path, fh):
        return rpyc.connect('localhost', self.port).root.flush(path,fh)

    def release(self, path, fh):
        return rpyc.connect('localhost', self.port).root.release(path,fh)

    def fsync(self, path, fdatasync, fh):
        return rpyc.connect('localhost', self.port).root.fsync(path,fdatasync,fh)

