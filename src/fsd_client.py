import rpyc
c=rpyc.connect('localhost',9487)
print c.root.sum(1,2)
c.close()