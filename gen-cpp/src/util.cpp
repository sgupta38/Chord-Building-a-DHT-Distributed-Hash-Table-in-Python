#include "util.h"

string get_sha256_hash(const string fileName)
{
	stringstream ss;

	if(0 != fileName.length())
	{
		ifstream file(fileName.c_str());
		unsigned char hash[SHA256_DIGEST_LENGTH];

		SHA256_CTX sha256;
		SHA256_Init(&sha256);
		
		if(file.is_open())
		{
			string line;
			while(getline(file, line))
			{
				SHA256_Update(&sha256, line.c_str(), line.size());
				line.clear();
			}

			SHA256_Final(hash, &sha256);
		}
		else
		{
			cout<<"\n Cant Open File";
			return "-1";
		}

		for(int i = 0; i < SHA256_DIGEST_LENGTH; i++)
		{
					ss << hex << setw(2) << setfill('0') << (int)hash[i];
		}
	}

	return ss.str();
}
