from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract():
    try:
        url = request.json['url']
        result = subprocess.run(
            ['yt-dlp', '-f', 'best', '-g', url],
            capture_output=True, text=True
        )
        return jsonify({
            'stream_url': result.stdout.strip(),
            'error': result.stderr.strip()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
