import rpyc
<<<<<<< HEAD:src/Client.py
c=rpyc.connect('localhost',9487)
print (c.root.sum(1,2))
c.close()
=======
c=rpyc.connect('localhost',2222)
print (c.root.sum(1,2))
c.close()
>>>>>>> 63063a28ae7e7f71a461d56978bfa812bd941994:src/fsd_client.py
