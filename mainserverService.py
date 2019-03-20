#!/usr/bin/env python3

from __future__ import with_statement

import os
import sys
import errno
import rpyc
import shutil
import random

from fuse import FUSE, FuseOSError, Operations

ROOT_DIR = "/tmp/mainserver/" # directory to store user-subserver relation information
subserver = {2510: ('localhost', 2510), 2511: ('localhost', 2511), 2512: ('localhost', 2512)} # subserver dictionary: {port: (address, port)}
duplicate_num = 2 # number of replications for each file

class Mainserver(rpyc.Service):
    def __init__(self):
        # create root directiory for main server
        if not os.path.isdir(ROOT_DIR):
            os.mkdir(ROOT_DIR)

    class exposed_MainService(object):
        def __init__(self, user_info):
            self.username = user_info
            self.return_value = {} # {returnValue of base_server: [(serverID, returnValue), ...]}

            # generate subserver list for this user
            self.sub_ser = self.select_sub()

        # load subserver information for old user
        # randomly select subservers for new user and record user-subserver relations
        def select_sub(self):
            # load user-subserver relation information
            try:
                user_file = open("/tmp/mainserver/user", 'r')
            except:
                user_file = open("/tmp/mainserver/user", 'w+')
            for i in user_file:
                if self.username in i: # if user-subserver relation has been built
                    sub_lis = i.strip('\n').split(' ')
                    user_file.close()
                    del sub_lis[0]
                    return sub_lis
            user_file.close()

            # if user-subserver relation hasn't been built
            user_file = open("/tmp/mainserver/user", 'a+')
            sub_lis = random.sample(subserver.keys(), duplicate_num)
            tmp_str = str(self.username)
            for sub in sub_lis:
                tmp_str += (' ' + str(sub))
            tmp_str += '\n'
            user_file.write(tmp_str) # record user-subserver relation
            user_file.close()
            
            return sub_lis

        # connect to subserver according to sub_id
        def connect_sub(self, sub_id):
            try:
                sub_addr, sub_port = subserver[int(sub_id)]
                return rpyc.connect(sub_addr, sub_port).root.SubserverService(sub_port, self.username)
            except:
                del self.sub_ser[sub_id]
                return None

        ######################
        # Filesystem methods #
        ######################
        # operations are forward to selected subservers
        # operations are finished by selected subservers

        def exposed_access(self, path, mode):
            for subserver_id in self.sub_ser:
                try:
                    self.connect_sub(subserver_id).access(path,mode)
                except:
                    continue

        def exposed_chmod(self, path, mode):
            for subserver_id in self.sub_ser:
                try:
                    returnValue = self.connect_sub(subserver_id).chmod(path,mode)
                except:
                    continue
            return returnValue

        def exposed_chown(self, path, uid, gid):
            for subserver_id in self.sub_ser:
                try:
                    returnValue = self.connect_sub(subserver_id).chown(path,uid,gid)
                except:
                    continue
            return returnValue

        def exposed_getattr(self, path, fh=None):
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

        def exposed_readdir(self, path, fh):
            for subserver_id in self.sub_ser:
                try:
                    returnValue = self.connect_sub(subserver_id).readdir(path,fh)
                except:
                    continue
            return returnValue

        def exposed_readlink(self, path):
            for subserver_id in self.sub_ser:
                try:
                    returnValue = self.connect_sub(subserver_id).readlink(path)
                except:
                    continue
            return returnValue

        def exposed_mknod(self, path, mode, dev):
            for subserver_id in self.sub_ser:
                try:
                    returnValue = self.connect_sub(subserver_id).mknod(path,mode,dev)
                except:
                    continue
            return returnValue

        def exposed_rmdir(self, path):
            for subserver_id in self.sub_ser:
                try:
                    returnValue = self.connect_sub(subserver_id).rmdir(path)
                except:
                    continue
            return returnValue

        def exposed_mkdir(self, path, mode):
            for subserver_id in self.sub_ser:
                try:
                    returnValue = self.connect_sub(subserver_id).mkdir(path,mode)
                except:
                    continue
            return returnValue

        def exposed_statfs(self, path):
            for subserver_id in self.sub_ser:
                try:
                    returnValue = self.connect_sub(subserver_id).statfs(path)
                except:
                    continue
            return returnValue

        def exposed_unlink(self, path):
            for subserver_id in self.sub_ser:
                try:
                    returnValue = self.connect_sub(subserver_id).unlink(path)
                except:
                    continue
            return returnValue

        def exposed_symlink(self, name, target):
            for subserver_id in self.sub_ser:
                try:
                    returnValue = self.connect_sub(subserver_id).symlink(name,target)
                except:
                    continue
            return returnValue

        def exposed_rename(self, old, new):
            for subserver_id in self.sub_ser:
                try:
                    returnValue = self.connect_sub(subserver_id).rename(old,new)
                except:
                    continue
            return returnValue

        def exposed_link(self, target, name):
            for subserver_id in self.sub_ser:
                try:
                    returnValue = self.connect_sub(subserver_id).link(target,name)
                except:
                    continue
            return returnValue

        def exposed_utimens(self, path, times=None):
            for subserver_id in self.sub_ser:
                try:
                    returnValue = self.connect_sub(subserver_id).utimens(path,times)
                except:
                    continue
            return returnValue

        ################
        # File methods #
        ################
        # operations are forward to selected subservers
        # operations are finished by selected subservers

        def exposed_open(self, path, flags):
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

        def exposed_create(self, path, mode, fi=None):
            #print("path: ", path)
            return_list = []
            #subserver_lis = self.pick_subserver()
            for subserver in self.sub_ser:
                try:
                    return_list.append((subserver, self.connect_sub(subserver).create(path, mode, fi)))
                except:
                    continue
            self.return_value[path] = return_list
            return return_list[0][1]

        def exposed_read(self, path, length, offset, fh):
            for subserver, fhandle in self.return_value[path]:
                try:
                    return self.connect_sub(subserver).read(path,length,offset,fhandle)
                except:
                    continue

        def exposed_write(self, path, buf, offset, fh):
            return_bytes = 0
            for subserver, sub_fh in self.return_value[path]:
                try:
                    return_bytes = self.connect_sub(subserver).write(path, buf, offset, sub_fh)
                except:
                    continue
            return return_bytes

        def exposed_truncate(self, path, length, fh=None):
            return_bytes = 0
            for subserver, sub_fh in self.return_value[path]:
                try:
                    return_bytes = self.connect_sub(subserver).truncate(path, length, sub_fh)
                except:
                    continue
            return return_bytes

        def exposed_flush(self, path, fh):
            return_bytes = 0
            for subserver, sub_fh in self.return_value[path]:
                try:
                    return_bytes = self.connect_sub(subserver).flush(path, sub_fh)
                except:
                    continue
            return return_bytes

        def exposed_release(self, path, fh):
            return_bytes = 0
            for subserver, sub_fh in self.return_value[path]:
                try:
                    return_bytes = self.connect_sub(subserver).release(path, sub_fh)
                except:
                    continue
            return return_bytes

        def exposed_fsync(self, path, fdatasync, fh):
            return_bytes = 0
            for subserver, sub_fh in self.return_value[path]:
                try:
                    return_bytes = self.connect_sub(subserver).fsync(path, fdatasync, sub_fh)
                except:
                    continue
            return return_bytes