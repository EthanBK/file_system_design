#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import errno
import rpyc
import shutil
import random

from fuse import FUSE, FuseOSError, Operations

class serverService(rpyc.Service):
    def __init__(self, addrList):
        self.addrList = addrList
        self.userList = []

    def get_user_info(self, user_info):
        self.userList.append(user_info)
        for addr in self.addrList:
            new_dir = os.path.join(addr, user_info)
            #print("New directory created: ", new_dir)
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)


    ##################
    # Help functions #
    ##################
    def get_root(self, path, user_info):
        for r in self.addrList:
            len_r = len(r)
            extracted = path[:len_r]
            if extracted == r:
                return r
        print("Error: get_root failed!")
            
    def _full_path(self, partial, user_info,creatingDir = False):
        partial = partial.lstrip("/")
        #check if the path exists in any server
        for addr in self.addrList:
            user_path = os.path.join(addr, user_info)
            path = os.path.join(user_path, partial)
            if(os.path.exists(path)):
                return path

        for addr in self.addrList:
            user_path = os.path.join(addr, user_info)
            path = os.path.join(user_path, partial)
            getDir = os.path.dirname(path)
            if os.path.exists(getDir) and (user_path != getDir):
                return path

        #if not, we'll need to assign a path from random server
        user_path = os.path.join(self.addrList[random.randint(0, len(self.addrList) - 1)], user_info)
        path = os.path.join(user_path, partial)
        return path


    ######################
    # Filesystem methods #
    ######################

    def access(self, path, mode, user_info):
        full_path = self._full_path(path, user_info)
        #print("access: ", full_path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode, user_info):
        full_path = self._full_path(path, user_info)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid, user_info):
        full_path = self._full_path(path, user_info)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, user_info, fh=None):
        full_path = self._full_path(path, user_info)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid', 'st_blocks'))

    def readdir(self, path, fh, user_info):
        dirents = ['.', '..']
        path = path.lstrip("/")
        for addr in self.addrList:
            addr_user = os.path.join(addr, user_info)
            full_path = os.path.join(addr_user, path)
            if os.path.isdir(full_path):
                dirents.extend(os.listdir(full_path))
        for r in list(set(dirents)):
            yield r

    def readlink(self, path, user_info):
        pathname = os.readlink(self._full_path(path, user_info))
        if pathname.startswith("/"):
            #print("=======here is the problem=======")
            return os.path.relpath(pathname, self.get_root(pathname, user_info))
        else:
            return pathname

    def mknod(self, path, mode, dev, user_info):
        return os.mknod(self._full_path(path, user_info), mode, dev)

    def rmdir(self, path, user_info):
        full_path = self._full_path(path, user_info)
        return os.rmdir(full_path)

    def mkdir(self, path, mode, user_info):
        #print("mkdir full path: ", self._full_path(path, user_info))
        return os.mkdir(self._full_path(path, user_info), mode)

    def statfs(self, path, user_info):
        full_path = self._full_path(path, user_info)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path, user_info):  # File remove
        #print(f"Remove: {path}\n")
        return os.unlink(self._full_path(path, user_info))

    def symlink(self, name, target, user_info):
        return os.symlink(name, self._full_path(target, user_info))

    def rename(self, old, new, user_info):
        return os.rename(self._full_path(old, user_info), self._full_path(new, user_info))

    def link(self, target, name, user_info):
        #print("FuseFunc->link:", target, name)
        return os.link(self._full_path(target, user_info), self._full_path(name, user_info))

    def utimens(self, path, user_info, times=None):
        return os.utime(self._full_path(path, user_info), times)


    ################
    # File methods #
    ################

    def open(self, path, flags, user_info):
        #print(f"Open: {path}\n")
        full_path = self._full_path(path, user_info)
        #print("open full path: ", full_path)
        return os.open(full_path, flags)

    def create(self, path, mode, user_info, fi=None):
        #print(f"Create: {path}\n")
        full_path = self._full_path(path, user_info)
        #print("create full path: ", full_path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh, user_info):
        #print(f"Read: {path}\n")
        #full_path = self._full_path(path, user_info)
        #print("read full path: ", full_path)

        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh, user_info):
        #print(f"Write: {path}\n")
        #full_path = self._full_path(path, user_info)
        #print("write full path: ", full_path)

        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, user_info, fh=None):
        #print(f"Truncate: {path}\n")
        full_path = self._full_path(path, user_info)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh, user_info):
        #print(f"Flush: {path}\n")
        return os.fsync(fh)

    def release(self, path, fh, user_info):
        #print(f"Release: {path}\n")
        return os.close(fh)

    def fsync(self, path, fdatasync, fh, user_info):
        #print(f"Fsync: {path}\n")
        return self.flush(path, fh, user_info)
