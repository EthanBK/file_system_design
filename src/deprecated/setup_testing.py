import rpyc 

mconn = rpyc.connect('localhost', 2220).root
sconn = rpyc.connect('localhost', 2220).root

print(mconn.print_one())

