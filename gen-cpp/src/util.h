#include <iostream>
#include <string>
#include <openssl/sha.h>
#include <fstream>
#include <vector>
#include <iterator>
#include <sstream>
#include <iomanip>
using namespace std;

string get_sha256_hash(const string fileName);