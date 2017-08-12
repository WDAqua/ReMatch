#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./webService.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import main as base
import urllib
import json

class S(BaseHTTPRequestHandler):
    
    initialized = False
    
    def init(self):
        if not self.initialized:
            self.initialized = True
            print('init started')
            self.mat=base.np.load('mat.dat')
            self.maxLength=base.np.load('maxLength.dat')
            self.glove = base.load_data('glove.dat')
            self.patty = base.load_data('patty.dat')
            self.patty.processData()
            print("data loaded")
    
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if not '.' in self.path[-4:]:
            self.init()
            self._set_headers()
            question = urllib.unquote(self.path[1:])
            #self.wfile.write("<html><body><h1>"+question+"</h1></body></html>")
            vectors, parts, pos, gen_question, similarities, unweighted, weighted, result, apiResults = base.processQuestion(self.glove,self.maxLength, self.patty, self.mat, question)
            o={}
            #o["vectors"]=[]
            #for vec in vectors:
            #	o["vectors"].append(vec.tolist())
            o["parts"]=parts
            o["pos"]=pos
            o["gen_question"]=gen_question
            results = [res[0] for res in result[:5]]
            if apiResults:
                i = 0
                for part in parts:
                    key = 'relation %d' % (i+1)
                    o[key] = results[i]
                    i += 1
            o["results"]=results
            self.wfile.write(json.dumps(o, indent=4, sort_keys=True))

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
       content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
       post_data = self.rfile.read(content_length) # <--- Gets the data itself
       print post_data # <-- Print post data
       self._set_headers()
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()