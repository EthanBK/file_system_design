import rpyc
import sys
import os
import argparse


def put(source, target):
    print("Calling put operation...")
    print("sSurce: ", source)
    print("Target: ", target)
    file_size = os.path.getsize(source)


    
    
def get(source, target):
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


    if args.operation == 'put':
        put(args.source, args.target)

    if args.operation == 'get':
        get(args.source, args.target)
        





