from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import threading

#Create custom HTTPRequestHandler class
class KodeFunHTTPRequestHandler(BaseHTTPRequestHandler):
    
    #handle GET command
    def do_GET(self):
        rootdir = 'c:/xampp/htdocs/' #file location
        try:
            #send code 200 response
            self.send_response(200)

            #send header first
            self.send_header('Content-type','text-html')
            self.end_headers()

            #send file content to client
            self.wfile.write("ciao".encode())
            return
            
        except IOError:
            self.send_error(404, 'errore')
    
def run():
    print('http server is starting...')

    #ip and port of servr
    #by default http server port is 80
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, KodeFunHTTPRequestHandler)
    print('http server is running...')
    httpd.serve_forever()
    
if __name__ == '__main__':
    http_thread = threading.Thread(target=run)
    http_thread.start()
