/*
 * @author: Sonu Gupta
 * @pupose: This acts as a "Test client". Sending dummy data to check connection is made or not.
 */

#include <iostream>
#include <vector>
#include <string>
#include "../gen-cpp/FileStore.h"
#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/server/TSimpleServer.h>
#include <thrift/transport/TServerSocket.h>
#include <thrift/transport/TBufferTransports.h>
#include <thrift/transport/TSocket.h>
#include <thrift/transport/TTransportUtils.h>

using namespace std;
using namespace ::apache::thrift;
using namespace ::apache::thrift::protocol;
using namespace ::apache::thrift::transport;
using namespace ::apache::thrift::server;
using boost::shared_ptr;


int main(int argc, char **argv) 
{
	std::cout<<"\n Client is up"<<std::endl;
	boost::shared_ptr<TTransport> socket(new TSocket(argv[1], std::stoi(argv[2])));
	boost::shared_ptr<TTransport> transport(new TBufferedTransport(socket));
	boost::shared_ptr<TProtocol> protocol(new TBinaryProtocol(transport));


	std::cout <<"Connection is set:"  << std::endl;

	try
	{
		FileStoreClient client(protocol);
		transport->open();
		RFile resourceFile;

		RFileMetadata resourceMetaData;
		vector<NodeID> nodes;
		NodeID nodeID; 
		resourceMetaData.contentHash = "dummyhash";
		resourceMetaData.filename = "apache.txt";
		resourceMetaData.version = 1;


		resourceFile.content = "RPC is best";
		resourceFile.meta = resourceMetaData;

		client.writeFile(resourceFile);
		string tempstring = "Test String";
		client.readFile(resourceFile, tempstring.c_str());
		client.setFingertable(nodes);
		client.findSucc(nodeID, tempstring.c_str());
		client.findPred(nodeID, tempstring.c_str());
		client.getNodeSucc(nodeID);
		transport->close();
	}
	catch(TException& e)
	{
		std::cout <<"ERROR: "<< e.what() << std::endl;
	}

return 0;
}

