import http.server
import socketserver
import os

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"message": "Hello from MedPredict API!", "status": "success"}')
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "healthy", "message": "API is working"}')
        else:
            super().do_GET()

port = int(os.environ.get('PORT', 5000))
with socketserver.TCPServer(("", port), MyHandler) as httpd:
    print(f"Server running on port {port}")
    httpd.serve_forever()
