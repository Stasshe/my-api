import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/fetch', methods=['GET'])
def fetch_page():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    try:
        response = requests.get(url)
        return jsonify({'content': response.text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # localhostで実行
