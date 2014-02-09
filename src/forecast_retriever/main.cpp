#include <iostream>

#include "msl/socket.hpp"

#include "msl/socket_util.hpp"

#include "get_request.hpp"

int main()
{
	std::cout<<"|"<<std::endl<<make_get_request_header("oisdjf","iosdjfoisdjf/")<<"|"<<std::endl;

	return 0;
}