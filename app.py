from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Video Extractor API is running! Use /extract endpoint"

@app.route('/extract', methods=['GET'])
def extract():
    try:
        url = request.args.get('url')
        if not url:
            return jsonify({"error": "Add ?url=YOUTUBE_URL to your request"}), 400
            
        result = subprocess.run(
            ['yt-dlp', '-f', 'best', '-g', url],
            capture_output=True, text=True, timeout=30
        )
        return jsonify({
            "stream_url": result.stdout.strip(),
            "error": result.stderr.strip()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
