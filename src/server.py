#
# @author: Sonu Gupta
# @pupose: This file has all the routines that are handled by a 'server'
# It implements various RPC functions.


import glob
import sys
sys.path.append('gen-py')
sys.path.insert(0, glob.glob('/home/yaoliu/src_code/local/lib/lib/python2.7/site-packages')[0])
from pathlib import Path

from chord import FileStore
import hashlib
import socket
from chord.ttypes import SystemException, RFileMetadata, RFile, NodeID

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

# Global variable for storing file ids:
fileId = {}
current_node = ''
IsFileOwned = False
same_key_node_name = False
#===========================================================================================================
#
# HELPER Functions
#
#===========================================================================================================

def calculate256hash(data):
    return hashlib.sha256(data.encode('utf8')).hexdigest()

def createFile(filename, content):
       # print('inside createFile')
        rFile = RFile()
        meta = RFileMetadata('',0,'')
        rFile.meta = meta
 
        try:
        #check if file exits or not.

            key = calculate256hash(filename)
            if key in fileId.keys():                          # if exists, open, override, increment version.
               # print('File Already exists')
                #Load previous version
                rFile = fileId[key]
                f = open(filename, "w")
                f.write(content)
                ## Somewhere, need to store this in memory. What if another client connects, we have to keep record of last number.
                rFile.meta.version = (int(rFile.meta.version) + 1)  
                rFile.meta.contentHash = calculate256hash(content)
                rFile.content = content
            else:
                ## Doesn't exist, so creating new file.

                f = open(filename, "w")
                f.write(content)
                rFile.meta.version = 0
                rFile.meta.filename = filename
                rFile.meta.contentHash = calculate256hash(content)
                rFile.content = content
               # print("Successfully created file")

            return rFile
        except:
               print('Error in createFile()')


def IsInRange(key, id1, id2):
    if key == id1 or key == id2:
        return True
    if id1 > id2:                    # This case is used for example 9->[21,19]
        if key > id1 or key < id2:
            return True
        else:
            return False               #e.g, 9->[21,30]
    elif id1 < id2:
        if key > id1 and key < id2:
            return True
        else:
            return False
    else:
# id1==id2
        print('Exception id1=id2')

        

def closet_preceding_finger(instance, key):
      # print('closet_preceding_finger() called')

       for node in reversed(instance.node_list):
           res = IsInRange(node.id, instance.currentNode.id, key)
           if res:
               node.port = int(node.port)
               return node

       return instance.currentNode

def connect_to_node_fp(ip, port, key):

#    print( 'connect_to_node_fp() called...')
    transport = TSocket.TSocket(ip, port)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = FileStore.Client(protocol)

    transport.open()
    node = NodeID('','',0)
    node =   client.findPred(key) 
    transport.close()
    return node

def connect_to_node_gs(ip, port, key):

 #   print( 'connect_to_node_gs() called...')
    transport = TSocket.TSocket(ip, port)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = FileStore.Client(protocol)

    transport.open()
    node = NodeID('','',0)
    node =   client.getNodeSucc() 
    transport.close()
    return node

#====================================================================================================================
#
#           Class Functions
#
#====================================================================================================================

class FileStoreHandler:
    def __init__(self):
        self.node_list = {}
        self.currentNode = NodeID('', '', 0)

    def getNodeSucc(self):
        print('getNodeSucc() called..')
        return self.node_list[0]
    
    def writeFile(self, rFile):
        print('writeFile() called..')
        global IsFileOwned
        global same_key_node_name

    #Delme: remove unwanted function calls

        key = calculate256hash(rFile.meta.filename)
        test_node = self.findSucc(key)
        if test_node != self.currentNode:
            IsFileOwned = False


        if same_key_node_name and test_node == self.currentNode:
            IsFileOwned = True

        # If 'SUCCESSOR', create file and add entry to 'In-memory File Content Table'
        # If 'NOT SUCCESSOR', raise a system exception.

        if IsFileOwned:
            rFile1 =  createFile(rFile.meta.filename, rFile.content)

        # Adding entry to the 'In-memory File Content Table' [FileID data structure] 
        
            fileId[calculate256hash(rFile.meta.filename)] = rFile1

            IsFileOwned = False  # Flag reset
        else:
            x = SystemException()
            x.message = 'This Server is not the SUCCESSOR of given file'
            raise x

        print()

    def readFile(self, filename):
        print('readFile() called..')
        global IsFileOwned
        global same_key_node_name
        key = calculate256hash(filename)
        test_node = self.findSucc(key)

        if test_node != self.currentNode:
     #       print('File is not owned by me')
            IsFileOwned = False

        if same_key_node_name and test_node == self.currentNode:
            IsFileOwned = True
        # If file is owned, check 'In-memory File Content Table'.
        # If 'successor' but file not yet written, raise exception
        # If NOT successor, raise exception

        if IsFileOwned:
            print()
            IsFileOwned = False  # Flag reset
            
            key = calculate256hash(filename)
            if key not in fileId.keys():
                x = SystemException()
                x.message = 'This server is SUCEESOR of file. But, File is not available yet.'
                raise x
            else:
                rfile = RFile()
                rfilemetadata = RFileMetadata('',0,'')
                rfile = fileId[key]
                return rfile
        else:
            x = SystemException()
            x.message = 'This Server is not the SUCCESSOR of given file'
            raise x

        print()
        
    def setFingertable(self, node_list):
        print('setFingertable() called..')
        self.node_list = node_list           # This is setting Finger Table.
        self.currentNode.ip = host_addr 
        self.currentNode.port = int(port)
        self.currentNode.id = current_node
        ''' 
        array_length = len(node_list)

        print(array_length)
        for i in range(len(node_list)):
            print(str(i) + ' ' + node_list[i].id + ' ' + node_list[i].ip + ' ' + str(node_list[i].port))
        '''


    def findSucc(self, key):
        print('findSucc() called..')
        global IsFileOwned
        global same_key_node_name


        array_length = len(self.node_list)
        if array_length == 0:
            x = SystemException()
            x.message = 'Finger Table is Empty'
            raise x

        p_node = NodeID('','',0)
        p_node =  self.findPred(key)

        if self.currentNode == p_node:
            if same_key_node_name:
                return self.currentNode
            else:
                s_node = self.node_list[0]
        elif p_node.id == key:
            return p_node
        else:
            s_node = connect_to_node_gs(p_node.ip, p_node.port, key)
            
            if s_node == self.currentNode:
                IsFileOwned = True
            else:
                IsFileOwned = False
            
        return s_node

    def findPred(self, key):
        print('findPred() called..')
        global same_key_node_name
        global IsFileOwned
        
        same_key_node_name = False
        IsFileOwned = False
        
        node = NodeID('','',0)

        node = self.currentNode

        firstEntry = self.node_list[0].id

        result = IsInRange(key, self.currentNode.id, firstEntry)
        if result:
            IsFileOwned = True

            if self.currentNode.id == key:   # special case key == node id
                same_key_node_name = True

            return self.currentNode
        else:                                         # Doesnt belongs to first index, start traversing from reverse. 
            #@note: use find pred on this returned value.[ Recursive ]
            returned_node = closet_preceding_finger(self, key)
            if self.currentNode == returned_node:
                possible_node =  connect_to_node_fp(self.node_list[0].ip, self.node_list[1].port, key)
                return possible_node
            else:                                      # connect to returned client, call its predecessor.
                # Check if server is not making an RPC call to itself. This might hang the server.
                
                if returned_node.ip == self.currentNode.ip and returned_node.port == self.currentNode.port:
                    return returned_node
                else:
                    possible_node =  connect_to_node_fp(returned_node.ip, returned_node.port, key)
                    return possible_node
            

    #Main Routine:
if __name__ == '__main__':
    handler = FileStoreHandler()
    processor = FileStore.Processor(handler)
    transport = TSocket.TServerSocket(port=int(sys.argv[1]))
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    host_addr = socket.gethostbyname(socket.gethostname())
    port = sys.argv[1]
    current_node_data = host_addr +':'+port 
    current_node = calculate256hash(current_node_data)
    print('server IP: ', host_addr)
    print('server Port: ', port)
    print('node_hash: ', current_node)

    print('Server is Started...')
    server.serve()
    print('Done')
