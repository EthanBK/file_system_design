import rpyc
c=rpyc.connect('localhost',2222)
print (c.root.sum(1,2))
c.close()
