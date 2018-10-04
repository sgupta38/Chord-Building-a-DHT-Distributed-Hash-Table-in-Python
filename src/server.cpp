/*
 * @author: Sonu Gupta
 * @purpose: This acts as a server.
 */


#include <iostream>
#include <string>

// These are necessary thrift header files
#include "../gen-cpp/FileStore.h"
#include <thrift/transport/TSocket.h>
#include <thrift/server/TThreadedServer.h>
#include <thrift/transport/TServerSocket.h>
#include <thrift/concurrency/ThreadManager.h>
#include <thrift/concurrency/PlatformThreadFactory.h>

#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/server/TSimpleServer.h>
#include <thrift/transport/TServerSocket.h>
#include <thrift/transport/TBufferTransports.h>
#include<boost/make_shared.hpp>


using namespace std;
using namespace apache::thrift;
using namespace apache::thrift::concurrency;
using namespace apache::thrift::protocol;
using namespace apache::thrift::transport;
using namespace apache::thrift::server;


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


class FileStoreCloneFactory : virtual public FileStoreIfFactory {
	 public:
		   virtual ~FileStoreCloneFactory() {}
		     virtual FileStoreIf* getHandler(const ::apache::thrift::TConnectionInfo& connInfo)
			 {
		       boost::shared_ptr<TSocket> sock = boost::dynamic_pointer_cast<TSocket>(connInfo.transport);
		       cout << "Incoming connection\n";
		       cout << "\tSocketInfo: "  << sock->getSocketInfo() << "\n";
			   cout << "\tPeerHost: "    << sock->getPeerHost() << "\n";
			   cout << "\tPeerAddress: " << sock->getPeerAddress() << "\n";
			   cout << "\tPeerPort: "    << sock->getPeerPort() << "\n";
			   return new FileStoreHandler;
			 }

			 virtual void releaseHandler( ::FileStoreIf* handler) 
			 {
			   delete handler;
			 } 
};

int main(int argc, char **argv) 
{

	// TTthreadedServer creates a single thread for each connected client. 
	TThreadedServer server(
			    boost::make_shared<FileStoreProcessorFactory>(boost::make_shared<FileStoreCloneFactory>()),
			    boost::make_shared<TServerSocket>(stoi(argv[1])), //port
			    boost::make_shared<TBufferedTransportFactory>(),
			    boost::make_shared<TBinaryProtocolFactory>()
				);

	try{
		  server.serve();
	  }catch(TException& e)
	  {
		  cout<<"\n ERROR:"<<e.what()<<endl;
	  }


    cout<<"Server is on...\n"<<endl;
	return 0;
}

