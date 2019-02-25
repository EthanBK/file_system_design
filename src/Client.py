import rpyc
import sys
import os
import argparse

def put(source, target):
    print(source, target)
    pass


if __name__ == "__main__":
    # Parse in arguments
    parser = argparse.ArgumentParser(description="Distributed File SYstem Client")
    parser.add_argument('-o', '--operation', required=True, help="Select operation: put or get")
    parser.add_argument('-s', '--source', required=True, help="Source file location")
    parser.add_argument('-t', '--target', required=True, help="File mount point")
    args = parser.parse_args()

    # Build connection
    con = rpyc.connect("localhost", port=2220)


    if args.operation == 'put':
        put(args.source, args.target)





