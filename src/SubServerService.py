import rpyc
import uuid
import os
import configparser
from time import sleep
import threading
import errno

from rpyc.utils.server import ThreadedServer
from fuse import FUSE, FuseOSError

ROOT_DIR = "/tmp/subserver/"

class SubServerService(rpyc.Service):


    #def on_connect(self, conn):
     #   print("subserver connected")

    #def on_disconnect(self, conn):
     #   print("subserver disconnected")
    def __init__(self, port):
        self.port = port
        self.root = ROOT_DIR + str(self.port) + '/'
        if not os.path.isdir(self.root):
            os.mkdir(self.root)
        self.active = True

    def get_status(self):
        return self.active

    def get_full_path(self, path):
        path = path.lstrip('/')
        return self.root + path

    ####################
    # Directory Method #
    ####################
    def access(self, path, mode):
        print(f"Access: {path}\n")
        full_path = self.get_full_path(path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        full_path = self.get_full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        full_path = self.get_full_path(path)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):
        full_path = self.get_full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        full_path = self.get_full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            yield r

    def readlink(self, path):
        pathname = os.readlink(self.get_full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        return os.mknod(self.get_full_path(path), mode, dev)

    def rmdir(self, path):
        full_path = self.get_full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        return os.mkdir(self.get_full_path(path), mode)

    def statfs(self, path):
        full_path = self.get_full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path):
        return os.unlink(self.get_full_path(path))

    def symlink(self, name, target):
        return os.symlink(name, self.get_full_path(target))

    def rename(self, old, new):
        return os.rename(self.get_full_path(old), self.get_full_path(new))

    def link(self, target, name):
        return os.link(self.get_full_path(target), self.get_full_path(name))

    def utimens(self, path, times=None):
        return os.utime(self.get_full_path(path), times)


    ###############
    # File Method #
    ###############
    def open(self, path, flags):
        print(f"Open: {path}\n")
        full_path = self.get_full_path(path)
        print(f"Full path: {full_path}\n")
        return os.open(full_path, flags)
    
    def create(self, path, mode, fi=None):
        print(f"Create: {path}\n")
        full_path = self.get_full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        print("read: ", path, length, offset, fh)
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        print("write: ", path, buf, offset, fh)
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        full_path = self.get_full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        return os.fsync(fh)

    def release(self, path, fh):
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        return self.flush(path, fh)
        

    # def exposed_write(self, block_id, data):
    #     """write data to the block in subserver"""
    #     f = open(self.dir + str(block_id), "w")
    #     f.write(data)

    # def exposed_read(self, block_id):
    #     """Return block content"""
    #     block_address = self.dir + str(block_id)
    #     if not os.path.isfile(block_address):
    #         return None
    #     fname = open(block_address)
    #     return fname.read()

    # def exposed_delete_file(self, block_id):
    #     """Remove block with block_id"""
    #     block_address = self.dir + str(block_id)
    #     if not os.path.isfile(block_address):
    #         return "Warning: No such file!"
    #     os.remove(block_address)
    #     return 0


# if __name__ == "__main__":
#     if not os.path.isdir(ROOT_DIR):
#         os.mkdir(ROOT_DIR)
    
#     cur_folder = os.path.dirname(os.path.abspath(__file__))
    