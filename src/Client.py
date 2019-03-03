import rpyc
import sys
import os
import argparse

###################################
# Architecture from Hadoop Distributed File System (HDFS)
#
# https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html
#
###################################

# Function: send_to_subserver(block_id, data, sub_server)
# Parameters:
#     <block_id>:  Main server service object
#     <source>:   Source file path
#     <target>:   Target location of mount
# Return:
#     None

def send_to_subserver(block_id, data, sub_server):
    # while(len(sub_servers) > 0):
        # next_server = sub_servers[0]
        # sub_servers = sub_servers[1:]
    con_server = rpyc.connect('localhost', sub_server).root.Subserver(sub_server)
    con_server.write(block_id, data)

def read_from_subserver(block_id, sub_server):
    con_server = rpyc.connect('localhost', sub_server).root.Subserver(sub_server)
    return con_server.read(block_id)

def delete_subserver_file(block_id, sub_server):
    con_server = rpyc.connect('localhost', sub_server).root.Subserver(sub_server)
    res =  con_server.delete_file(block_id)
    if res != 0:
        print(res)



# Funciton: put(service, source, target)
# Parameters:
#     <service>:  Main server service object
#     <source>:   Source file path
#     <target>:   Target location of mount
# Return:
#     None
def put(service, source, target):
    print("Calling put operation...")
    print("Source: ", source)
    print("Target: ", target)
    # Get file size
    file_size = os.path.getsize(source)
    # Get (block id, subserver id) tuple
    block_table = service.creat_file_table_entry(target, file_size)
    # print('block_table', block_table)
    # Split data and put into blocks
    with open(source) as fp:
        for tpl in block_table: # only one b in blocks for now
            data = fp.read()    # For new, read all data
            block_uuid = tpl[0]
            # get sub server object
            #sub_servers = service.get_sub_server(b[1])
            for s in tpl[1]:
                subserver = s
                # send to sub server
                send_to_subserver(block_uuid, data, subserver)
        
    
# Funciton: put(service, source, target)
# Parameters:
#     <service>:  Main server service object
#     <source>:   File source
#     <target>:   Target location of mount
# Return:
#     None
def get(service, target):
    print("Calling get operation...")
    print("Target: ", target)
    block_table = service.get_file_table(target)
    print(block_table)
    if not block_table:
        print("Error: No Such File.")
        return
    data = None
    for tpl in block_table: # size(block) == 1 for now
        for server in tpl[1]:
            data = read_from_subserver(tpl[0], server)
            if data:
                sys.stdout.write(data)
                break
            print("Warning: data missing on block", tpl[0], ". Searching on other sub-server")
        if not data:
            print("Error: Cannot find data on all sub-servers. Getting data failed.")
    
def delete(service, target):
    print("Calling delete operation...")
    print("Target: ", target)
    block_table = service.get_file_table(target)
    if not block_table:
        print("Error: No Such File.")
        return

    for tpl in block_table:
        for server in tpl[1]:
            delete_subserver_file(tpl[0], server)

    service.delete_file(target)
    print("Target delete successfully.")
            

def rename(service, oldname, newname):
    print("Calling rename operation...")
    print("Old name: ", oldname)
    print("New name: ", newname)

    blocks_table = service.get_file_table(oldname)
    if not blocks_table:
        print("Error: No Such File.")
        return
    service.rename_file(oldname, newname)


if __name__ == "__main__":
    # Parse in arguments
    parser = argparse.ArgumentParser(description="Distributed File SYstem Client")
    parser.add_argument('-o', '--operation', required=True, help="Select operation: put or get")
    parser.add_argument('-s', '--source', required=False, help="Source file location")
    parser.add_argument('-t', '--target', required=True, help="File mount point")
    parser.add_argument('-p', '--port', required=True, help="Port number")
    args = parser.parse_args()

    # Build connection\
    port = int(args.port)
    con = rpyc.connect("localhost", port = port)
    main_server_service_exposed = con.root.MainServer()


    if args.operation == 'put':
        put(main_server_service_exposed, args.source, args.target)

    if args.operation == 'get':
        get(main_server_service_exposed, args.target)

    if args.operation == 'rename':
        rename(main_server_service_exposed, args.source, args.target)

    if args.operation == 'del':
        delete(main_server_service_exposed, args.target)
