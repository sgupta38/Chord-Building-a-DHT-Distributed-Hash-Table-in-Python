#
# @author: Sonu Gupta
# @purpose: This file has all the routines of 'findSucc'

import sys
import glob
import hashlib
sys.path.append('gen-py')
sys.path.insert(0, glob.glob('/home/yaoliu/src_code/local/lib/lib/python2.7/site-packages')[0])

from chord import FileStore
from chord.ttypes import SystemException, RFileMetadata, RFile, NodeID

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
def calculate256hash(data):
    return hashlib.sha256(data.encode('utf8')).hexdigest()


def main():
    transport = TSocket.TSocket(sys.argv[1], int(sys.argv[2]))
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = FileStore.Client(protocol)

    transport.open()
    
## findSucc

    try:
        print("findSucc() called..") 
        suc =  client.findSucc(calculate256hash('hello.txt'))
        print('  suc id: ', suc.id)
        print('  suc ip: ', suc.ip)
        print('  suc port: ', suc.port)
        print()
    except SystemException as e:
        print('SystemException: %r' % e)
	
    transport.close()
    
if __name__ == '__main__':
    try:
        main()
    except Thrift.TException as tx:
        print('%s' % tx.message)

