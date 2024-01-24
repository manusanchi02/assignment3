import http.client as httplib
import sys

#get http server ip
http_server = "http://localhost:8080"
url = "/"
#create a connection
conn = httplib.HTTPConnection(http_server)

while 1:    
    #request command to server
    conn.request("GET", url)

    #get response from server
    rsp = conn.getresponse()
    
    #print server response and data
    print(rsp.status, rsp.reason)
    data_received = rsp.read()
    print(data_received)
    
conn.close()