from http.server import SimpleHTTPRequestHandler, HTTPServer
import requests
import os
import re

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
                response = requests.get(url)
                html_content = response.content
                # リソースのパスを相対パスに変換
                html_content = self.convert_resource_links(html_content, url)
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(html_content)
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f'Error: {str(e)}'.encode())
        elif self.path.startswith('/proxy'):
            # プロキシ用のGETリクエストを処理
            self.do_PROXY()
        else:
            # その他のGETリクエストの処理
            if self.path == '/':
                self.path = 'index.html'
            return super().do_GET()

    def convert_resource_links(self, html_content, base_url):
        """HTML内のリソースリンクを相対パスに変換する"""
        html_content = html_content.decode('utf-8')
        # CSSや画像のリンクを相対パスに変換
        html_content = re.sub(r'(?i)(href|src)="(http[s]?://[^"]+)"', r'\1="/proxy?url=\2"', html_content)
        return html_content.encode('utf-8')

    def do_PROXY(self):
        # プロキシ用のGETリクエストを処理
        url = self.path.split('?url=')[1]
        response = requests.get(url)
        self.send_response(200)
        self.send_header('Content-Type', response.headers['Content-Type'])
        self.end_headers()
        self.wfile.write(response.content)

def run(server_class=HTTPServer, handler_class=RequestHandler):
    port = int(os.environ.get('PORT', 8000))  # 環境変数からポートを取得
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
