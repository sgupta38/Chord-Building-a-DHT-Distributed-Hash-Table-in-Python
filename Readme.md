# Chord : Distributed Hash Table
-----------------------------------------------------------------------
##### A FILE SERVER implementation based on distributed hash table(DHT) protocol with an architecture similar to the Chord system. 
-----------------------------------------------------------------------
## Overview:

##### Example: 
If ten nodes are in the DHT running on 10 different ports on “128.226.117.49:9090”, ...,
“128.226.117.49:9099”, and we want to write the a file “example.txt”, owned by “guest”, then the key
associated with this file SHA256(“guest:example.txt”)=“ad0c...” must be written to the node associated with the
next SHA-256 value in the Chord id space. According to the Chord DHT specification (shown in below figure), this
node is “128.226.117.49:9093’, which has an SHA-256 hash of “c529...”.

![alt text](https://github.com/Yao-Liu-CS457-CS557/cs457-cs557-pa2-sgupta38/blob/master/images/dht.png)

Every time the server is started the filesystem is initialized to be empty.The server stores files in the file system,and for simplicity it uses the current working directory from where it was run. This implementation did not implement the directory structure. In addition, the server executable takes a single command-line argument specifying the port where the Thrift service will listen for remote clients. For example:
   ./server 9090
It uses the Thrift’s TBinaryProtocol for marshalling and unmarshalling data structures. Multiple servers can run at the same time. 

#### 1. Compile the interface definition file

   $> thrift -gen py chord.thrift

#### 2. Extending the server-side method stubs generated by Thrift
1. writeFile() given a name, owner, and contents, the corresponding file should be written to the server. Meta information, such as the owner, version, and content hash (use the SHA-256 hash) should also be stored at the server side.

2. readFile() if a file with a given name and owner exists on the server, both the contents and meta-information should
be returned. Otherwise, a SystemException should be thrown and appropriate information indicating the
cause of the exception should be included in the SystemException’s message field.

3. setFingertable() sets the current node’s fingertable to the fingertable provided in the argument of the function. The init program that will call this function, but you need to correctly implement this function on the server side.

4. findSucc() given an identifier in the DHT’s key space, returns the DHT node that owns the id.

5. findPred() given an identifier in the DHT’s key space, this function should returns the DHT node that immediately
precedes the id. This preceeding node is the first node in the counter-clockwise direction in the Chord key
space.

6.getNodeSucc() returns the closest DHT node that follows the current node in the Chord key space.

#### 3. Run the initializer program
 
 > chmod +x init
 > 
 > ./init node.txt
   > 
The file (node.txt) should contain a list of IP addresses and ports, in the format “<ip-address>:<port>”, of all of the running DHT nodes.

For example, if four DHT nodes are running on remote01.cs.binghamton.edu port 9090, 9091, 9092,
and 9093, then nodes.txt should contain:
  128.226.180.163:9090,
  128.226.180.163:9091,
  128.226.180.163:9092,
  128.226.180.163:9093,
  
The initializer program will print an error message if any of the specified DHT nodes is not available.

#### 4. Test the File Server:

I have written the indivisual test_clients to check the functionality of each RPC call. If you want to 'Write' a file, call write_client.py and to 'Read' a file, call read_client.py. You have to explicitly provide 'ip' and 'port' each time.

To automate the testing, I have written some scripts which calls each of these clients and executes RPC calls based on user selection. The only prerequisite is to have valid 'node.txt' file and one command line argument which acts as 'Filename' in front of 'mytest.sh' script.

> ./mytest.sh hello.txt
> 
> Please enter a test to check.
> 1. WriteFile
> 2. ReadFile
> 3. FindSucc
> 4. FindPred
> 5. getNodeSucc


-----------------------------------------------------------------------


## Instructions to execute.
1. thrift -gen py chord.thrift
2. ./server.sh <port_no>
3. ./init node.txt 

-----------------------------------------------------------------------

## Brief Description:
The Server is implemented in Python.

### server.py (src/)
1. server.py takes 'Port' as command line argument and listens on it.
2. It implements six different methods as mentioned earlier.
3. Each request to server is served on different thread.
4. Server stores the fingure-table and the file's metadata information.
5. It throws SystemException in case the unauthorized file access request. 

### Test_clients(present in src/test_clients)
1. This directory has 5 files to test DHT impementation.


### Sample Input/Output:
----------------------------------------------------------------------
![alt text](https://github.com/Yao-Liu-CS457-CS557/cs457-cs557-pa2-sgupta38/blob/master/images/all.png)

WriteFile()

![alt text](https://github.com/Yao-Liu-CS457-CS557/cs457-cs557-pa2-sgupta38/blob/master/images/writefile.png)

ReadFile()

![alt text](https://github.com/Yao-Liu-CS457-CS557/cs457-cs557-pa2-sgupta38/blob/master/images/readfile.png)

FindSucc()

![alt text](https://github.com/Yao-Liu-CS457-CS557/cs457-cs557-pa2-sgupta38/blob/master/images/findsucc.png)

FindPred()

![alt text](https://github.com/Yao-Liu-CS457-CS557/cs457-cs557-pa2-sgupta38/blob/master/images/findpred.png)

getNodeSucc()

![alt text](https://github.com/Yao-Liu-CS457-CS557/cs457-cs557-pa2-sgupta38/blob/master/images/getnodesucc.png)