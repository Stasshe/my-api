from http.server import SimpleHTTPRequestHandler, HTTPServer
import requests
import os

class RequestHandler(SimpleHTTPRequestHandler):
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
                # 指定されたURLからHTMLを取得
                response = requests.get(url)
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')  # HTMLとして返す
                self.end_headers()
                self.wfile.write(response.content)  # 取得したHTMLをそのまま返す
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f'Error: {str(e)}'.encode())
        else:
            if self.path == '/':
                self.path = 'index.html'
            return super().do_GET()

def run(server_class=HTTPServer, handler_class=RequestHandler):
    port = int(os.environ.get('PORT', 8000))  # 環境変数からポートを取得
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
