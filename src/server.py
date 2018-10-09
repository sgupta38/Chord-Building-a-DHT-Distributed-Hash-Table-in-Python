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

from chord.ttypes import SystemException, RFileMetadata, RFile, NodeID

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

# Global variable for storing file ids:
fileId = {}
fingerTable = {}

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


#====================================================================================================================
#
#           Class Functions
#
#====================================================================================================================

class FileStoreHandler:

    def writeFile(self, rFile):
        print()
        print('writeFile called()')
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

    def readFile(self, filename):
        print('readFile called()')

## Initially check whether this file exists or not. if not, throw exception
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
        array_length = len(node_list)

        print(array_length)
        for i in range(array_length):
            fingerTable[i] = node_list[i].id
        #    print('id: ',node_list[i].id)
         #   print('ip: ',node_list[i].ip)
          #  print('port: ',node_list[i].port)

        print('Finger Table: ', fingerTable)

   ## key will be given, so find the SUCCESSOR ,
   #  print all info and 
   #  return 

    def findSucc(self, key):
        print('findSucc called()')
        r_nodeid =  NodeID()
        r_nodeid.id = 'xxx'
        r_nodeid.ip = '127.0.0.1'
        r_nodeid.port = 9090

        return r_nodeid

   ## key will be given, so find the PREDECESSOR
    # print all info and 
    # return 

    def findPred(self, key):
        print('findPred called()')
        r_nodeid =  NodeID()
        r_nodeid.id = 'yyy'
        r_nodeid.ip = '127.0.0.2'
        r_nodeid.port = 4636

        return r_nodeid

    ## return the succesor
    def getNodeSucc(self):
        print('getNodeSucc called()')


    #Main Routine:
if __name__ == '__main__':
    handler = FileStoreHandler()
    processor = FileStore.Processor(handler)
    transport = TSocket.TServerSocket(port=int(sys.argv[1]))
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)


    print('Starting the server')
    server.serve()
    print('Done')
        

