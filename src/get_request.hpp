#ifndef GET_REQUEST_HPP
#define GET_REQUEST_HPP

#include <string>

void separate_host_and_file(const std::string& url,std::string& host,std::string& file);

std::string make_get_request_header(const std::string& client,const std::string& url);

#endif