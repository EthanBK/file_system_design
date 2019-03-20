# File System Design
# Secured Distributed File System (SDFS)

##  Dependecies

-  Python >=3.4
-   Rpyc package (pip install rpyc)
-   Fusepy package (pip install fusepy)

##  Run SDFS
### 1. Create Mount Point
Create an empty directory (e.g. `virtual`) as the mount point under the same directory of `client.py`.

`mkdir virtual`

### 2. Start Sub Servers
In three terminals, run three sub servers:

`python3 subserver.py`

Then enter the port number (2510, 2511 and 2512) for each sub server:

`Input the port for the Subserver: 2510`

The following message should show up:

```
IP: localhost
Port: 2510
Starting sub server service...
```

### 3. Start Main Server
In a new terminal, run `mainserver.py`:

`python3 mainserver.py`

Then enter the port number (e.g. 2220):

`Input the port for the Mainserver: 2220`

The following message should show up:

```
IP: localhost
Port: 2220
Starting main server service...
```

### 4. Start Client
In a new terminal, run `client.py`:

`python3 client.py [-v] [-p]`


**Parameters**

| Short        | Long           | Description  |
| ------------ |:--------------:| ------------ |
| -v      | --virtual | Virtual file system mount point |
| -p      | --port | Port setting for the main server (e.g. 2220)|
| -d     | --address | Address setting for the main server (e.g. 'localhost')|

## Change Parameters
Parameters are located in `mainserverService.py` as shown below:

```
ROOT_DIR =  "/tmp/mainserver/"

subserver = {2510: ('localhost', 2510), 2511: ('localhost', 2511), 2512: ('localhost', 2512)}

duplicate_num =  2
```

`ROOT_DIR` specifies the directory for main server to store user/subserver information

`subserver` hard code the sub server list

`duplicate_num` specifies the number of replications for each file

## Supported Functions
Directory functions:
 - Create directory
 - Remove directory
 - Copy/paste/move directory
 - Rename directory
 
File functions:
 - Create fire
 - Write to file
 - Read from file
 - Rename file
 - Delete file
 - Copy/paste/move file

## Features

 1. Isolated user environment
 
Each user has access only to its own directories/files.

2. Hidden sub server

Sub servers are selected and controlled by the main server and are invisible to users.

3. File replication

Each file is replicated certain times (specified by developer) and stored in different sub servers randomly.
