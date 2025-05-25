from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    try:
        # Handle both GET and POST requests
        if request.method == 'GET':
            url = request.args.get('url')
        else:
            url = request.json.get('url')
        
        if not url:
            return jsonify({"error": "URL parameter is required"}), 400

        result = subprocess.run(
            ['yt-dlp', '-f', 'best', '-g', url],
            capture_output=True, text=True, timeout=30
        )
        
        return jsonify({
            "stream_url": result.stdout.strip(),
            "error": result.stderr.strip()
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Video extraction timed out"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
