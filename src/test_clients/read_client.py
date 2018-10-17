#
# @author: Sonu Gupta
# @purpose: This file has all the routines of 'readFile'

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


## readFile

    #todo: handle return type
    try:
        _ret =  client.readFile(sys.argv[3]);

        print("readFile() called..") 
        print('  FileName: ', _ret.meta.filename)
        print('  Version: ', _ret.meta.version)
        print('  Content Hash: ', _ret.meta.contentHash)
        print('  Content: ', _ret.content)
        print()
    except SystemException as e:
        print(e)

    transport.close()
if __name__ == '__main__':

    try:
        main()
    except Thrift.TException as tx:
        print('%s' % tx.message)

