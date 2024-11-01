from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
import os

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/fetch'):
            query = self.path.split('?')[1] if '?' in self.path else ''
            params = dict(q.split('=') for q in query.split('&') if '=' in q)
            url = params.get('url', '')

            if not url:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'URL is required')
                return

            try:
                response = requests.get(url)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'content': response.text}).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())

    def log_message(self, format, *args):
        return  # Disable logging

def run(server_class=HTTPServer, handler_class=RequestHandler):
    port = int(os.environ.get('PORT', 8000))
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
