#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import errno
import rpyc
import shutil

from pathlib import Path
from fuse import FUSE, FuseOSError, Operations

FILE_DIR = "/home/roger/Desktop/ECS251/tbmounted/"


class subService(rpyc.Service):
    def __init__(self):
        self.root = FILE_DIR
        #self.subserverRootDir = rpyc.connect('localhost',port)

    def getRoot(self):
        return self.root
        
    def connection_test(self):
        return self.active

    def _full_path(self, partial):
        partial = partial.lstrip("/")
        path = os.path.join(self.root, partial)
        return path

    def access(self, path, mode):
        full_path = self._full_path(path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    def readdir(self, path, fh):
        path = str(Path(FILE_DIR))

        for r in os.listdir(path):
            yield r

    def mkdir(self, path, mode):
        return os.mkdir(self._full_path(path), mode)


    def getattr(self, path, fh=None):
        #print("FileSystem method: getattr\n")
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def statfs(self, path):
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def chmod(self, path, mode):
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)


    def unlink(self, path):  # File remove
        print(f"Remove: {path}\n")
        return os.unlink(self._full_path(path))

    def rename(self, old, new):
        return os.rename(self._full_path(old), self._full_path(new))

    def utimens(self, path, times=None):
        return os.utime(self._full_path(path), times)


    # File methods
    # ============

    def open(self, path, flags):
        print(f"Open: {path}\n")
        full_path = self._full_path(path)
        return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        print(f"Create: {path}\n")
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        print(f"Read: {path}\n")
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        print(f"Write: {path}\n")
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        print(f"Truncate: {path}\n")
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        print(f"Flush: {path}\n")
        return os.fsync(fh)

    def release(self, path, fh):
        print(f"Release: {path}\n")
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        print(f"Fsync: {path}\n")
        return self.flush(path, fh)

    def migrate(self,toHost):
        zipFile = "/server/data_store/backup"
        print("Packing migration data...")
        shutil.make_archive(zipFile, 'zip', FILE_DIR)  # Zip server files

        print("Sending migration data...")
        with open(zipFile + ".zip", 'rb') as f:
            data = f.read()
            rpyc.connect(host=toHost,port=18861).root.acceptMigrate(data)

        os.remove(self._full_path("backup.zip"))
        print("Migration complete...")

    def acceptMigrate(self,data):
        zipFile = "/server/data_store/backup.zip"

        print("Receiving migration data...")
        f = open(zipFile,'wb')
        f.write(data)
        f.close()

        print("Unpacking migration data...")
        shutil.unpack_archive(zipFile, extract_dir=FILE_DIR)

        os.remove(self._full_path("backup.zip"))
        print("Migration complete...")

    def shutdown(self):
        print("Shuttind down...")
        self.active = False
        exit(0)