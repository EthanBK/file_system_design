import rpyc
import sys
import os
import argparse


"""
Funciton: put(service, source, target)
Parameters:
    <service>:  Main server service object
    <source>:   File source
    <target>:   Target location of mount
Return:
    None
"""
def put(service, source, target):
    print("Calling put operation...")
    print("sSurce: ", source)
    print("Target: ", target)
    file_size = os.path.getsize(source)
    


"""
Funciton: put(service, source, target)
Parameters:
    <service>:  Main server service object
    <source>:   File source
    <target>:   Target location of mount
Return:
    None
"""
def get(service, source, target):
    print("Calling get operation...")
    print("sSurce: ", source)
    print("Target: ", target)

if __name__ == "__main__":
    # Parse in arguments
    parser = argparse.ArgumentParser(description="Distributed File SYstem Client")
    parser.add_argument('-o', '--operation', required=True, help="Select operation: put or get")
    parser.add_argument('-s', '--source', required=True, help="Source file location")
    parser.add_argument('-t', '--target', required=True, help="File mount point")
    parser.add_argument('-p', '--port', required=True, help="Port number")
    args = parser.parse_args()

    # Build connection\
    port = args.port
    con = rpyc.connect("localhost", port=port)
    main_server_service_exposed = con.root.MainServer()


    if args.operation == 'put':
        put(main_server_service_exposed, args.source, args.target)

    if args.operation == 'get':
        get(main_server_service_exposed, args.source, args.target)
        





