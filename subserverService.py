#!/usr/bin/env python3

from __future__ import with_statement

import os
import sys
import errno
import rpyc
import shutil
import random

from fuse import FUSE, FuseOSError, Operations

ROOT_DIR = "/tmp/subserver/"

class Subserver(rpyc.Service):
    def __init__(self, port):
        # create the root directory
        if not os.path.isdir(ROOT_DIR):
            os.mkdir(ROOT_DIR)
        self.addr = ROOT_DIR + str(port) +'/'
        if not os.path.isdir(self.addr):
            os.mkdir(self.addr)

        self.port = port
        self.exposed_port = port

    class exposed_SubserverService(object):
        def __init__(self, port, username):
            self.address = ROOT_DIR + str(port) + '/' + str(username) + '/'

            # create individual directory for each user
            if not os.path.isdir(self.address):
                os.mkdir(self.address)
            self.root = None

        ##################
        # Help functions #
        ##################

        # map virtual path in the mount point to real path in the subserver
        def _full_path(self, partial, creatingDir = False):
            partial = partial.lstrip("/")
            path = os.path.join(self.address, partial)
            return path

        ######################
        # Filesystem methods #
        ######################
        # finish the operation from client

        def exposed_access(self, path, mode):
            full_path = self._full_path(path)
            if not os.access(full_path, mode):
                raise FuseOSError(errno.EACCES)

        def exposed_chmod(self, path, mode):
            full_path = self._full_path(path)
            return os.chmod(full_path, mode)

        def exposed_chown(self, path, uid, gid):
            full_path = self._full_path(path)
            return os.chown(full_path, uid, gid)

        def exposed_getattr(self, path, fh=None):
            full_path = self._full_path(path)
            st = os.lstat(full_path)
            return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                         'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid', 'st_blocks'))

        def exposed_readdir(self, path, fh):
            full_path = self._full_path(path)

            dirents = ['.', '..']
            if os.path.isdir(full_path):
                dirents.extend(os.listdir(full_path))
            for r in dirents:
                yield r

        def exposed_readlink(self, path):
            pathname = os.readlink(self._full_path(path))
            if pathname.startswith("/"):
                print("=======here is the problem=======")
                return os.path.relpath(pathname, self.root)
            else:
                return pathname

        def exposed_mknod(self, path, mode, dev):
            return os.mknod(self._full_path(path), mode, dev)
 
        def exposed_rmdir(self, path):
            full_path = self._full_path(path)
            return os.rmdir(full_path)

        def exposed_mkdir(self, path, mode):
            #print("cur path: ", path)
            return os.mkdir(self._full_path(path), mode)

        def exposed_statfs(self, path):
            full_path = self._full_path(path)
            stv = os.statvfs(full_path)
            return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
                'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
                'f_frsize', 'f_namemax'))

        def exposed_unlink(self, path):  # File remove
            #print(f"Remove: {path}\n")
            return os.unlink(self._full_path(path))

        def exposed_symlink(self, name, target):
            return os.symlink(name, self._full_path(target))

        def exposed_rename(self, old, new):
            return os.rename(self._full_path(old), self._full_path(new))

        def exposed_link(self, target, name):
            #print("FuseFunc->link:", target, name)
            return os.link(self._full_path(target), self._full_path(name))

        def exposed_utimens(self, path, times=None):
            return os.utime(self._full_path(path), times)


        ################
        # File methods #
        ################
        # finish the operation from client

        def exposed_open(self, path, flags):
            #print(f"Open: {path}\n")
            full_path = self._full_path(path)
            return os.open(full_path, flags)


        def exposed_create(self, path, mode, fi=None):
            #print(f"Create: {path}\n")
            full_path = self._full_path(path)
            return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

        def exposed_read(self, path, length, offset, fh):
            #print(f"Read: {path}\n")
            os.lseek(fh, offset, os.SEEK_SET)
            return os.read(fh, length)
 
        def exposed_write(self, path, buf, offset, fh):
            #print(f"Write: {path}\n")
            return os.write(fh, buf)

        def exposed_truncate(self, path, length, fh=None):
            #print(f"Truncate: {path}\n")
            full_path = self._full_path(path)
            with open(full_path, 'r+') as f:
                f.truncate(length)

        def exposed_flush(self, path, fh):
            #print(f"Flush: {path}\n")
            return os.fsync(fh)

        def exposed_release(self, path, fh):
            #print(f"Release: {path}\n")
            return os.close(fh)

        def exposed_fsync(self, path, fdatasync, fh):
            #Sprint(f"Fsync: {path}\n")
            return self.exposed_flush(path, fh)