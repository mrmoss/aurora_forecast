#!/usr/bin/python

import SocketServer
import urllib
import db_util
import re
import test_kp_retreival

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.data=self.request.recv(1024).strip()
        
        request=self.data;
        #create character buffer for parsed_request
        #get second whitespace separated block
        parsed_request = 'GET [{"predicted_time":{"year":2014,"month": 4,"day": -1,"hour":-1,"minute":-1},"forecast":"d28"}] / HTTP 1.1 ';

        #get the substring
        parsed_sub_request = parsed_request[parsed_request.find("[")+1:parsed_request.find("]")]

	#add [] back into request so its a valid JSON object
	parsed_sub_request = "[" + parsed_sub_request + "]"
        
	#convert the request if we want
        #converted_request=urllib.unquote(parsed_sub_request).decode('utf8')


	#GET OUR DATA FROM THE DATABASE
	
	data = test_kp_retreival.get_data(parsed_sub_request)
	

        #service request
        #send modified JSON object
        self.request.sendall(data)

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8080

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
