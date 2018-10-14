#
# @author: Sonu Gupta
# @pupose: This file all the routines that are handled by a 'server'


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
#===========================================================================================================
#
# HELPER Functions
#
#===========================================================================================================

def calculate256hash(data):
    return hashlib.sha256(data.encode('utf8')).hexdigest()

def createFile(filename, content):
        print('inside createFile')
        rFile = RFile()
        meta = RFileMetadata('',0,'')
        rFile.meta = meta
 
#     try:
        #check if file exits or not.

        key = calculate256hash(filename)
        if key in fileId.keys():                          # if exists, open, override, increment version.
            print('File Already exists')
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
            print("Successfully created file")

        return rFile
 #    except:
 #           print('Error in createFile()')


def IsInRange(key, id1, id2):
    if key > id1 and key < id2:       # simple case e.g, 9->[8,20]
        print('Firsti case')
        return True
    elif id1 > id2:                    # This case is used for example 9->[21,19]
        if key < id1 and key < id2:
            print('Seocnd case')
            return True
        else:
            return Fals               #e.g, 9->[21,30]
    else:
        return False

def closet_preceding_finger(instance, key):
       print('closet_preceding_finger() called')
       print('size of Finger Table= ', len(instance.node_list))

       for node in reversed(instance.node_list):
           print(' Searching.. ')
           print(' between Current node: ', instance.currentNode.id)
           print(' Searching between TABLE Entry ', node.id)
           print(' Searching between KEY', key)
           res = IsInRange(node.id, instance.currentNode.id, key)
           if res:
               print(' closest preceding node is:', node.id)
               node.port = int(node.port)
               return node

       print('returning current node')
       return instance.currentNode

def connect_to_node_fp(ip, port, key):

    print( 'connect_to_node_fp() called...')
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

    print( 'connect_to_node_gs() called...')
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
        print('node list entry is', self.node_list[0]) # Returning the first entry
        return self.node_list[0]
    
    def writeFile(self, rFile):
        print('writeFile() called..')
        global IsFileOwned

    #Delme: remove unwanted function calls

        key = calculate256hash(rFile.meta.filename)
        print(' key is', key)
        test_node = self.findSucc(key)
        print(' test node:', test_node)
        print(' Is File Owned', IsFileOwned)

        # If 'SUCCESSOR', create file and add entry to 'In-memory File Content Table'
        # If 'NOT SUCCESSOR', raise a system exception.

        if IsFileOwned:
            rFile1 =  createFile(rFile.meta.filename, rFile.content)
            print('  FileName: ', rFile1.meta.filename)
            print('  Version: ', rFile1.meta.version)
            print('  Content Hash: ', rFile1.meta.contentHash)
            print('  Content : ', rFile1.content)

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
        key = calculate256hash(filename)
        test_node = self.findSucc(key)
        print(' Is File Owned', IsFileOwned)

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
        
        array_length = len(node_list)

        print(array_length)
        for i in range(len(node_list)):
            print(str(i) + ' ' + node_list[i].id + ' ' + node_list[i].ip + ' ' + str(node_list[i].port))


    def findSucc(self, key):
        print('findSucc() called..')
        global IsFileOwned
        p_node = NodeID('','',0)
        p_node =  self.findPred(key)

        if self.currentNode == p_node:
            print('Myself')
            s_node = self.node_list[0]
        else:
            print(' Connecting to..' )
            print(' ip: ', p_node.ip)
            print(' port: ', p_node.port)
            print(' id: ', p_node.id)

            s_node = connect_to_node_gs(p_node.ip, p_node.port, key)

            if s_node == self.currentNode:
                IsFileOwned = True
        
        return s_node

    def findPred(self, key):
        print('findPred() called..')
        global IsFileOwned
        node = NodeID('','',0)
        node = self.currentNode

        firstEntry = self.node_list[0].id

        #Delme: doubt

    #   if self.currentNode.id >= key  and key<= firstEntry:    # check with first index
        result = IsInRange(key, self.currentNode.id, firstEntry)
#        if self.currentNode.id <= key <= firstEntry:    # check with first index
        if result:
            print(' key is between current_node and fingerTable[0]')
            IsFileOwned = True
            return self.currentNode
        else:                                         # Doesnt belongs to first index, start traversing from reverse. 
            print(' Not in range. Traversing reverse.')
            #@note: use find pred on this returned value.[ Recursive ]
            returned_node = closet_preceding_finger(self, key)
            if self.currentNode == returned_node:
                print(' next closest is', returned_node)
                return self.currentNode
               # return self.node_list[0] #returning sucessor
            else:                                      # connect to returned client, call its predecessor.
                
                #@Delme: Comments
                print("Connecting to next hop and traversing its FingerTable")
                print('Trying to connect:')
                print('ip: ', returned_node.ip)
                print('port: ', returned_node.port)
                
                # Check if server is not making an RPC call to itself. This might hang the server.
                
                if returned_node.ip == self.currentNode.ip and returned_node.port == self.currentNode.port:
                    print('oopsssss its me')
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
    print(current_node_data)
    print('node_hash: ', current_node)

    print('Starting the server')
    server.serve()
    print('Done')
