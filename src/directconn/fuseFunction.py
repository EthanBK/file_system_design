#!/usr/bin/env python3

from __future__ import with_statement

import os
import sys
import errno
import rpyc
from pathlib import Path
from fuse import FUSE, FuseOSError, Operations

class FuseOperation(Operations):
    def __init__(self, root, addr_main, port_main):
        self.root = root        # tmp/subserver/2510
        # Access to main server
        self.main_service_conn = rpyc.connect(addr_main, port_main).root.Mainserver()

    def _full_path(self, path):
         # get subserver for this file (path)
         # subser_port = self.main_service_conn.find_subserver(path)
         path = path.lstrip('/')
         path = os.path.join(self.root, path)
         return path     # tmp/subserver/2510/test.txt

    def subserver_connect(self, subserver_id):
        addr_sub, port_addr = self.main_service_conn.subservers[subserver_id]
        return rpyc.connect(addr_sub, port_addr)

    ####################
    # Directory Method #
    ####################
    def access(self, path, mode):
        pass

    #def access(self, path, mode):
    #    print("FuseFunc->access:", path)
    #    if(path in self.main_service_conn.file_table):
    #        file_entry = self.main_service_conn.file_table[path]
    #        s_addr, s_port = self.main_service_conn.get_subserver[file_entry.subser_addr]
    #        return self.subserver_connect(s_addr, s_port).root.access(file_entry.r_path, mode)

    #def chmod(self, path, mode):
    #    print("FuseFunc->chmod:", path)
    #    file_entry = self.main_service_conn.file_table[path]
    #    s_addr, s_port = self.main_service_conn.get_subserver[file_entry.subser_addr]
    #    return self.subserver_connect(s_addr, s_port).root.access(file_entry.r_path, mode)

    #def chown(self, path, uid, gid):
    #    print("FuseFunc->chown:", path)
    #    file_entry = self.main_service_conn.file_table[path]
    #    s_addr, s_port = self.main_service_conn.get_subserver[file_entry.subser_addr]
    #    return self.subserver_connect(s_addr, s_port).root.chown(file_entry.r_path, uid, gid)

    def getattr(self, path, fh=None):
        print("FuseFunc->getattr:", path)
        if(path in self.main_service_conn.directories):
            full_path = self._full_path(path)
            st = os.lstat(full_path)
            return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                        'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
        
        print("path not in mainserver")
        for sub in self.main_service_conn.subservers.keys():
            try:
                r_path = self.main_service_conn.file_table[path].r_path
                return self.subserver_connect(sub).root.getattr(r_path, fh)
            except:
                pass
                #print("Exception 1 in fuseFunction.")

        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                    'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        print("FuseFunc->readdir:", path)
        if(path in self.main_service_conn.directories):
            
            fileList = []

            # Add files to fileList
            for sub in self.main_service_conn.subservers.keys():
                subserver_fileList = list(self.subserver_connect(sub).root.readdir('./', fh))
                for realPath in subserver_fileList:
                    file = self.main_service_conn.file_fromReal(realPath)
                    if(file is not None):
                        if(file.dir == path):
                            fileList.append(str(Path(file.v_path).name))

            # Add Directories to fileList
            if(path == '/'):
                for dir in self.main_service_conn.directories.keys():
                    if(dir == '/'):
                        continue
                    fileList.append(dir[1:])

            if(len(fileList) > 0):
                for r in fileList:
                    yield r

        #full_path = self._full_path(path)

        #dirents = ['.', '..']
        #if os.path.isdir(full_path):
        #    dirents.extend(os.listdir(full_path))
        #for r in dirents:
        #    yield r

    def readlink(self, path):
        print("FuseFunc->readlink:", path)
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    #def mknod(self, path, mode, dev):
    #    print("FuseFunc->mknod:", path)
    #    return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        print("FuseFunc->rmdir:", path)
        self.main_service_conn.remove_directory(path)
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        print("FuseFunc->mkdir:", path)
        self.main_service_conn.create_dictionary(path)

        return os.mkdir(self._full_path(path), mode)

    #def statfs(self, path):
    #    print("FuseFunc->statfs:", path)
    #    full_path = self._full_path(path)
    #    print("full path: ", full_path)
    #    stv = os.statvfs(full_path)
    #    return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
    #        'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
    #        'f_frsize', 'f_namemax'))

    def unlink(self, path):
        print("FuseFunc->unlink:", path)
        file = self.main_service_conn.file_table[path]
        sub = file.subser_addr
        self.subserver_connect(sub).root.unlink(file.r_path)
        self.main_service_conn.remove_file(path)
    #    return os.unlink(self._full_path(path))

    #def symlink(self, name, target):
    #    print("FuseFunc->symlink:", name, target)
    #    return os.symlink(name, self._full_path(target))

    #def rename(self, old, new):
    #    print("FuseFunc->rename:", old, new)
    #    return os.rename(self._full_path(old), self._full_path(new))

    #def link(self, target, name):
    #    print("FuseFunc->link:", target, name)
    #    return os.link(self._full_path(target), self._full_path(name))

    #def utimens(self, path, times=None):
    #    print("FuseFunc->utimens:", path)
    #    return os.utime(self._full_path(path), times)

    ###############
    # File Method #
    ###############
    
    def open(self, path, flags):
        print("FuseFunc->open:", path)
        file_entry = self.main_service_conn.file_table[path]
        subser = self.main_service_conn.get_subserver[file_entry.subser.port]
        return subser.get_connection().root.open(file_entry.r_path, flags)

    def create(self, path, mode, fi=None):
        print("FuseFunc->create:", path)
        file_entry = self.main_service_conn.createFile(path)
        subser = self.main_service_conn.get_subserver[file_entry.subser.port]
        return subser.get_connection().root.create(file_entry.r_path, mode, fi)

    def read(self, path, length, offset, fh):
        print("FuseFunc->read:", path)
        file_entry = self.main_service_conn.file_table[path]
        subser = self.main_service_conn.get_subserver[file_entry.subser.port]
        return subser.get_connection().root.read(file_entry.r_path, length, offset, fh)

    def write(self, path, buf, offset, fh):
        print("FuseFunc->write:", path)
        file_entry = self.main_service_conn.file_table[path]
        subser = self.main_service_conn.get_subserver[file_entry.subser.port]
        return subser.get_connection().root.write(file_entry.r_path, buf, offset, fh)

    def truncate(self, path, length, fh=None):
        print("FuseFunc->truncate:", path)
        file_entry = self.main_service_conn.file_table[path]
        subser = self.main_service_conn.get_subserver[file_entry.subser.port]
        return subser.get_connection().root.truncate(file_entry.r_path, length, fh)

    def flush(self, path, fh):
        print("FuseFunc->flush:", path)
        file_entry = self.main_service_conn.file_table[path]
        subser = self.main_service_conn.get_subserver[file_entry.subser.port]
        return subser.get_connection().root.flush(file_entry.r_path, fh)

    def release(self, path, fh):
        print("FuseFunc->release:", path)
        file_entry = self.main_service_conn.file_table[path]
        subser = self.main_service_conn.get_subserver[file_entry.subser.port]
        return subser.get_connection().root.release(file_entry.r_path, fh)

    def fsync(self, path, fdatasync, fh):
        print("FuseFunc->fsync:", path)
        file_entry = self.main_service_conn.file_table[path]
        subser = self.main_service_conn.get_subserver[file_entry.subser.port]
        return subser.get_connection().root.fsync(file_entry.r_path, fdatasync, fh)