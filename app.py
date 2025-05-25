@app.route('/extract', methods=['GET', 'POST'])  # Add 'GET' here
def extract():
    if request.method == 'GET':
        url = request.args.get('url')  # For GET: ?url=YOUR_URL
    else:
        url = request.json.get('url')  # For POST
    
    if not url:
        return jsonify({"error": "URL parameter missing"}), 400

    try:
        result = subprocess.run(
            ['yt-dlp', '-f', 'best', '-g', url],
            capture_output=True, text=True
        )
        return jsonify({
            "stream_url": result.stdout.strip(),
            "error": result.stderr.strip()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
