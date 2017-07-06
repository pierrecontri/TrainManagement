#!/usr/bin/python3

import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import http.server
 
PORT = 8888
server_address = ("10.0.2.82", PORT)

server = http.server.HTTPServer
handler = http.server.CGIHTTPRequestHandler
handler.cgi_directories = ["/"]
print("Server listening on port : %d", PORT)

httpd = server(server_address, handler)
try:
  httpd.serve_forever()
except KeyboardInterrupt:
  pass

print("Server stoped\nBye")

# ex in web browser : http://localhost:8888/TrainManagement.py?control=get_help&functionName=Switch&functionValue=Off
