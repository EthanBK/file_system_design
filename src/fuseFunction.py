#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import errno
import rpyc

from fuse import FUSE, FuseOSError, Operations

class FuseOperation(Operations):
    def __init__(self, root, controller):
        self.root = root        # src_dir/
        self.controller = controller

    def _full_path(self, path):
        path = path.lstrip('/')
        path = os.path.join(self.root, path)
        return path

    ####################
    # Directory Method #
    ####################
    def access(self, path, mode):
        if path in self.controller.file_table:
            file_entry = self.controller.file_table[path]
            subser = self.controller.get_subserver[file_entry.subser.port]
            return subser.get_connection().root.access(file_entry.r_path, mode)

    def chmod(self, path, mode):
        file_entry = self.controller.file_table[path]
        subser = self.controller.get_subserver[file_entry.subser.port]
        return subser.get_connection().root.chmod(file_entry.r_path, mode)

    def chown(self, path, uid, gid):
        file_entry = self.controller.file_table[path]
        subser = self.controller.get_subserver[file_entry.subser.port]
        return subser.get_connection().root.chown(file_entry.r_path, uid, gid)

    def getattr(self, path, fh=None):
        if path in self.controller.directory:
            full_path = self._full_path(path)
            st = os.lstat(full_path)
            return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                        'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
        else:
            for port in self.controller.subservers.keys():
                try:
                    r_path = self.controller.file_table[path].r_path
                    return self.controller.get_subserver(port).root.get_connection().root.getattr(r_path, fh)
                except:
                    print("Exception 1 in fuseFunction.")
            full_path = self._full_path(path)
            st = os.lstat(full_path)
            return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                        'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            yield r

    def readlink(self, path):
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path):
        return os.unlink(self._full_path(path))

    def symlink(self, name, target):
        return os.symlink(name, self._full_path(target))

    def rename(self, old, new):
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        return os.link(self._full_path(target), self._full_path(name))

    def utimens(self, path, times=None):
        return os.utime(self._full_path(path), times)

    ###############
    # File Method #
    ###############
    
    def open(self, path, flags):
        file_entry = self.controller.file_table[path]
        subser = self.controller.get_subserver[file_entry.subser.port]
        return subser.get_connection().root.open(file_entry.r_path, flags)

    def create(self, path, mode, fi=None):
        file_entry = self.controller.file_table[path]
        subser = self.controller.get_subserver[file_entry.subser.port]
        return subser.get_connection().root.create(file_entry.r_path, mode, fi)

    def read(self, path, length, offset, fh):
        file_entry = self.controller.file_table[path]
        subser = self.controller.get_subserver[file_entry.subser.port]
        return subser.get_connection().root.read(file_entry.r_path, length, offset, fh)

    def write(self, path, buf, offset, fh):
        file_entry = self.controller.file_table[path]
        subser = self.controller.get_subserver[file_entry.subser.port]
        return subser.get_connection().root.write(file_entry.r_path, buf, offset, fh)

    def truncate(self, path, length, fh=None):
        file_entry = self.controller.file_table[path]
        subser = self.controller.get_subserver[file_entry.subser.port]
        return subser.get_connection().root.truncate(file_entry.r_path, length, fh)

    def flush(self, path, fh):
        file_entry = self.controller.file_table[path]
        subser = self.controller.get_subserver[file_entry.subser.port]
        return subser.get_connection().root.flush(file_entry.r_path, fh)

    def release(self, path, fh):
        file_entry = self.controller.file_table[path]
        subser = self.controller.get_subserver[file_entry.subser.port]
        return subser.get_connection().root.release(file_entry.r_path, fh)

    def fsync(self, path, fdatasync, fh):
        file_entry = self.controller.file_table[path]
        subser = self.controller.get_subserver[file_entry.subser.port]
        return subser.get_connection().root.fsync(file_entry.r_path, fdatasync, fh)

