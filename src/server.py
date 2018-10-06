#
# @author: Sonu Gupta
# @pupose: This file all the routines that are handled by a 'server'


import glob
import sys
sys.path.append('gen-py')
sys.path.insert(0, glob.glob('/home/yaoliu/src_code/local/lib/lib/python2.7/site-packages')[0])

from chord import FileStore

from chord.ttypes import SystemException, RFileMetadata, RFile, NodeID

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


class FileStoreHandler:

    def writeFile(self, rFile):
        print('writeFile called()')
        print('  FileName: ', rFile.meta.filename)
        print('  Version: ', rFile.meta.version)
        print('  Content Hash: ', rFile.meta.contentHash)
        print('  Content : ', rFile.content)

    def readFile(self, filename):
        print('readFile called()')

        rfilemetadata = RFileMetadata()
        rfilemetadata.filename = 'test1.txt'
        rfilemetadata.version = 2
        rfilemetadata.contentHash = 'yyyyyyyyyyyyy'

        rfile = RFile()
        rfile.meta = rfilemetadata
        rfile.content = 'eeeeeeeeeeeeeeeeeeeeeeeeeee'
        return rfile

    def setFingertable(self, node_list):
        print('setFingertable called()')

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
        

