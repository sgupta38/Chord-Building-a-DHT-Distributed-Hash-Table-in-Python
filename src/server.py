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

def closet_preceding_finger(instance, key):
       print('closet_preceding_finger() called')
       print('size of Finger Table= ', len(instance.node_list))

       for node in reversed(instance.node_list):
           print('Searching.. ')
           print(' between Current node: ', instance.currentNode.id)
           print(' Searching between TABLE Entry ', node.id)
           print(' Searching between KEY', key)
           if instance.currentNode.id <= node.id <= key:
               print('closest preceding node is:', node.id)
               return node

       print('returning current node')
       return instance


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
        print('getNodeSucc called()')
        print('node list entry is', self.node_list[0]) # Returning the first entry
        return self.node_list[0]
    
    def writeFile(self, rFile):
        print()
        global IsFileOwned
        print('writeFile called()')

        # lets check whether findsucc() point to itself or node. If points, write file other wise raise exception and tell where it is.
        key = calculate256hash(rFile.meta.filename)
        print(' key is', key)
        test_node = self.findSucc(key)
        print(' test node:', test_node)
        print(' Is File Owned', IsFileOwned)

        # if both hashes are same, write file. If it already exists, update version and content.
        if IsFileOwned:
            print('Hash matches. File is owned by this server. Doing proper action.')
            rFile1 =  createFile(rFile.meta.filename, rFile.content)
            print('  FileName: ', rFile1.meta.filename)
            print('  Version: ', rFile1.meta.version)
            print('  Content Hash: ', rFile1.meta.contentHash)
            print('  Content : ', rFile1.content)
        # Adding entry to the FileID data structure.
            fileId[calculate256hash(rFile.meta.filename)] = rFile1

            print("FileID table:")
            print(fileId)
            print()
            IsFileOwned = False  # Flag reset
        else:
            x = SystemException()
            x.message = 'This Server Doesnt owns the file'
            raise x

        print()

    def readFile(self, filename):
        print()
        print('readFile called()')
        key = calculate256hash(filename)
        if key not in fileId.keys():
            x = SystemException()
            x.message = 'File Doesnt Exist'
            raise x
        else:
            rfile = RFile()
            rfilemetadata = RFileMetadata('',0,'')
            rfile = fileId[key]
            return rfile

    def setFingertable(self, node_list):
        print('setFingertable called()')
        self.node_list = node_list
        self.currentNode.ip = host_addr 
        self.currentNode.port = port
        self.currentNode.id = current_node
        
        array_length = len(node_list)

        print(array_length)
        for i in range(len(node_list)):
            print(str(i) + ' ' + node_list[i].id + ' ' + node_list[i].ip + ' ' + str(node_list[i].port))


    def findSucc(self, key):
        print('findSucc called')
        succ_node = NodeID('','',0)
        succ_node =  self.findPred(key)
        if self.currentNode == succ_node:
            print(" 1. This file is owned by MYSELF: ", succ_node)
        else:
            succ_node =  self.getNodeSucc() 
            print(" 2. This file is owned by: ", succ_node)
        
        return succ_node

    def findPred(self, key):
        print('findPred called()')
        global IsFileOwned

        firstEntry = self.node_list[0].id

        print('Firstly check with node and its first entry')
        print(' node  ', self.currentNode.id)
        print(' key   ', key)
        print(' First Entry', firstEntry)

        if self.currentNode.id <= key <= firstEntry:    # check with first index
            print(' key is between current_node and fingerArray at index 0')
            IsFileOwned = True
            print('eehaa')
            return self.currentNode
        else:                                       # Doesnt belongs to first index, start traversing from reverse. 
            print(' Not in range')
            #use find pred on this returned value.. recursive
            returned_node = closet_preceding_finger(self, key)
            if self == returned_node:
                print(' next closest is', returned_node)
                return self.currentNode
            else:
                print("Need to call recursive Functionn here")
                return self.currentNode
            

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
