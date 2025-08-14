import http.server
import socketserver
from functools import partial

Handler = partial(http.server.SimpleHTTPRequestHandler, directory="_site")

with socketserver.TCPServer(("", 1111), Handler) as httpd:
    print("serving at http://localhost:1111")
    httpd.serve_forever()
