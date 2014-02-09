#include "get_request.hpp"

std::string make_get_request_header(const std::string& client,const std::string& url)
{
	std::string url_server;
	std::string url_file;

	for(auto ii:url)
	{
		if(ii=='/')
			break;
		else
			url_server+=ii;
	}

	url_file=url.substr(url_server.size(),url.size()-url_server.size());

	std::string header;
	header+="GET "+url_file+" HTTP/1.1\n";
	header+="User-Agent: "+client+"\n";
	header+="Accept: */*\n";
	header+="Host: "+url_server+"\n";
	header+="Connection: Keep-Alive\r\n\n\r";

	return header;
}