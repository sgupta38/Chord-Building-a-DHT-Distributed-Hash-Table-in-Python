#
# @author: Sonu Gupta
# @purpose: This file has all the routines of 'client'

import sys
import glob
sys.path.append('gen-py')
sys.path.insert(0, glob.glob('/home/yaoliu/src_code/local/lib/lib/python2.7/site-packages')[0])

from chord import FileStore
from chord.ttypes import SystemException, RFileMetadata, RFile, NodeID

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

def main():
    transport = TSocket.TSocket(sys.argv[1], int(sys.argv[2]))
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = FileStore.Client(protocol)

    transport.open()
    print("getNodeSucc() called..") 
    next_node =  client.getNodeSucc()
    print("Next Node ip:", next_node.ip)
    print("Next Node port:", next_node.port)
    print("Next Node id:", next_node.id)



## writeFile
    rfile = RFile()
    rfileMetadata = RFileMetadata('',0,'') # NOTE: structure needs to be initialised with default values. otherwise, nonetype error.
    
    rfileMetadata.filename = 'hello.txt'
    rfile.meta = rfileMetadata
    rfile.content = 'This is text string..!!'
    print()

    try:
        client.writeFile(rfile);
        print("writeFile() called..") 
        print()
    except SystemException as e:
        print('SystemException: %r' % e)

## readFile

    #todo: handle return type
    try:
        _ret =  client.readFile('hello.txt');

        print("readFile() called..") 
        print('  FileName: ', _ret.meta.filename)
        print('  Version: ', _ret.meta.version)
        print('  Content Hash: ', _ret.meta.contentHash)
        print('  Content: ', _ret.content)
        print()
    except SystemException as e:
        print('SystemException: %r' % e)

'''
## findSucc

    try:
        suc =  client.findSucc('hello.txt')
        print("findSucc() called..") 
        print('  suc id: ', suc.id)
        print('  suc ip: ', suc.ip)
        print('  suc port: ', suc.port)
        print()
    except SystemException as e:
        print('SystemException: %r' % e)


## findPred

    try:
        pred = client.findPred('hello.txt')
        print("findPred() called..") 
        print('  pred id: ', pred.id)
        print('  pred ip: ', pred.ip)
        print('  pred  port: ', pred.port)
        print()
    except SystemException as e:
        print('SystemException: %r' % e)
'''
if __name__ == '__main__':
    try:
        main()
    except Thrift.TException as tx:
        print('%s' % tx.message)

