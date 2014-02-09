#include <iostream>

#include "msl/socket.hpp"

#include "msl/socket_util.hpp"

#include "get_request.hpp"

int main()
{
	std::string url="www.swpc.noaa.gov/ftpdir/weekly/27DO.txt";
	std::string host;
	std::string file;

	separate_host_and_file(url,host,file);

	msl::socket sock(msl::lookup_ip(host)+":80");

	sock.connect_tcp();

	if(sock.good())
	{
		std::cout<<":)"<<std::endl;
	}
	else
	{
		std::cout<<":("<<std::endl;
		exit(0);
	}

	std::string request=make_get_request_header("forecast_retriever",url);

	sock.write(request.c_str(),request.size());

	char b;

	while(sock.read(&b,1)==1)
		std::cout<<b;

	return 0;
}