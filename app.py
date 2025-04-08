# http hello world using ./index.html:
import http.server
import socketserver

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open("./index.html", "rb") as file:
            self.wfile.write(file.read())

