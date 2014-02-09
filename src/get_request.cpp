#include "get_request.hpp"

void separate_host_and_file(const std::string& url,std::string& host,std::string& file)
{
	host="";
	file="";

	for(auto ii:url)
	{
		if(ii=='/')
			break;
		else
			host+=ii;
	}

	file=url.substr(host.size(),url.size()-host.size());

}

std::string make_get_request_header(const std::string& client,const std::string& url)
{
	std::string url_host;
	std::string url_file;

	separate_host_and_file(url,url_host,url_file);

	std::string header;
	header+="GET "+url_file+" HTTP/1.1\r\n";
	header+="User-Agent: "+client+"\r\n";
	header+="Accept: */*\r\n";
	header+="Host: "+url_host+"\r\n";
	header+="Connection: Keep-Alive\r\n";
	header+="\r\n\n\r";

	return header;
}