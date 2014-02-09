#include <iostream>

#include "get_request.hpp"

int main()
{
	bool passed=true;

	std::string test_get_header="GET /test.html HTTP/1.1\nUser-Agent: Forecast-Retriever\nAccept: */*\nHost: www.google.com\nConnection: Keep-Alive\r\n\n\r";

	passed=(make_get_request_header("Forecast-Retriever","www.google.com/test.html")==test_get_header);

	if(passed)
		std::cout<<"Everything works!"<<std::endl;
	else
		std::cout<<"There was a problem!"<<std::endl;

	return 0;
}