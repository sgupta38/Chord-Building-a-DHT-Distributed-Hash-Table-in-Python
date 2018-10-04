// This autogenerated skeleton file illustrates how to build a server.
// You should copy it to another filename to avoid overwriting it.

#include "FileStore.h"
#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/server/TSimpleServer.h>
#include <thrift/transport/TServerSocket.h>
#include <thrift/transport/TBufferTransports.h>

using namespace ::apache::thrift;
using namespace ::apache::thrift::protocol;
using namespace ::apache::thrift::transport;
using namespace ::apache::thrift::server;

using boost::shared_ptr;

class FileStoreHandler : virtual public FileStoreIf {
 public:
  FileStoreHandler() {
    // Your initialization goes here
  }

  void writeFile(const RFile& rFile) {
    // Your implementation goes here
    printf("writeFile\n");
  }

  void readFile(RFile& _return, const std::string& filename) {
    // Your implementation goes here
    printf("readFile\n");
  }

  void setFingertable(const std::vector<NodeID> & node_list) {
    // Your implementation goes here
    printf("setFingertable\n");
  }

  void findSucc(NodeID& _return, const std::string& key) {
    // Your implementation goes here
    printf("findSucc\n");
  }

  void findPred(NodeID& _return, const std::string& key) {
    // Your implementation goes here
    printf("findPred\n");
  }

  void getNodeSucc(NodeID& _return) {
    // Your implementation goes here
    printf("getNodeSucc\n");
  }

};

/*

int main(int argc, char **argv) {
  int port = 9090;
  shared_ptr<FileStoreHandler> handler(new FileStoreHandler());
  shared_ptr<TProcessor> processor(new FileStoreProcessor(handler));
  shared_ptr<TServerTransport> serverTransport(new TServerSocket(port));
  shared_ptr<TTransportFactory> transportFactory(new TBufferedTransportFactory());
  shared_ptr<TProtocolFactory> protocolFactory(new TBinaryProtocolFactory());

  TSimpleServer server(processor, serverTransport, transportFactory, protocolFactory);
  server.serve();
  return 0;
}

*/