#!/usr/bin/env python3
import rpyc

from fuse import FUSE, FuseOSError, Operations

class Passthrough(Operations):
    def __init__(self, addr, port, user_info):
        self.addr = addr
        self.port = port
        self.user_info = user_info
        self.main_service = rpyc.connect(self.addr, self.port).root.MainService(user_info) # connect to main server

    ######################
    # Filesystem methods #
    ######################
    # operation requests are send to main server.
    # mainserver select subservers and forward operation requests to them.
    # selected subservers finish the operation

    # Check file access permissions
    def access(self, path, mode):
        self.main_service.access(path, mode)

    # Change the permission bits of a file
    def chmod(self, path, mode):
        return self.main_service.chmod(path, mode)

    # Change the owner and group of a file
    def chown(self, path, uid, gid):
        return self.main_service.chown(path, uid, gid)

    # Get file attributes.
    def getattr(self, path, fh=None):
        return self.main_service.getattr(path, fh)

    # Read directory
    def readdir(self, path, fh):
        return self.main_service.readdir(path, fh)

    # Read the target of a symbolic link
    def readlink(self, path):
        return self.main_service.readlink(path)

    # Create a file node
    def mknod(self, path, mode, dev):
        return self.main_service.mknod(path, mode, dev)

    # Remove a directory
    def rmdir(self, path):
        return self.main_service.rmdir(path)

    # Create a directory
    def mkdir(self, path, mode):
        return self.main_service.mkdir(path, mode)

    # Get file system statistics
    def statfs(self, path):
        return self.main_service.statfs(path)

    # Remove a file
    def unlink(self, path):
        return self.main_service.unlink(path)

    # Create a symbolic link
    def symlink(self, name, target):
        return self.main_service.symlink(name, target)

    # Rename a file
    def rename(self, old, new):
        return self.main_service.rename(old, new)

    # Create a hard link to a file
    def link(self, target, name):
        return self.main_service.link(target, name)

    # Change the access and modification times of a file with nanosecond resolution
    def utimens(self, path, times=None):
        return self.main_service.utimens(path, times)


    ################
    # File methods #
    ################
    # operation requests are send to main server.
    # mainserver select subservers and forward operation requests to them.
    # selected subservers finish the operation

    # Open a file
    def open(self, path, flags):
        return self.main_service.open(path, flags)

    # Create a file
    def create(self, path, mode, fi=None):
        #print("path: ", path)
        return self.main_service.create(path, mode, fi)

    # Read from a file
    def read(self, path, length, offset, fh):
        return self.main_service.read(path, length, offset, fh)

    # Write to a file
    def write(self, path, buf, offset, fh):
        return self.main_service.write(path, buf, offset, fh)

    # Change the size of a file
    def truncate(self, path, length, fh=None):
        return self.main_service.truncate(path, length, fh)

    # Possibly flush cached data
    def flush(self, path, fh):
        return self.main_service.flush(path, fh)

    # Release an open file
    def release(self, path, fh):
        return self.main_service.release(path, fh)

    # Synchronize file contents
    def fsync(self, path, fdatasync, fh):
        return self.main_service.fsync(path, fdatasync, fh)

