#include <iostream>

#include "get_request.hpp"

int main()
{
	bool passed=true;

	std::string test_get_header="GET /test.html HTTP/1.1\r\nUser-Agent: Forecast-Retriever\r\nAccept: */*\r\nHost: www.google.com\r\nConnection: Keep-Alive\r\n\r\n\n\r";

	passed=(make_get_request_header("Forecast-Retriever","www.google.com/test.html")==test_get_header);

	if(passed)
		std::cout<<"Everything works!"<<std::endl;
	else
		std::cout<<"There was a problem!"<<std::endl;

	return 0;
}