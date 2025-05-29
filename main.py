from fastapi import FastAPI, Request, HTTPException
import os
import subprocess

app = FastAPI()
API_KEY = os.getenv("API_KEY")

@app.post("/download")
async def download_video(request: Request):
    client_key = request.headers.get("X-API-KEY")
    if client_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key ❌")

    try:
        data = await request.json()
        video_url = data.get("url")
        if not video_url:
            return {"error": "No video URL provided"}

        # Try to download using yt-dlp
        result = subprocess.run(
            ["yt-dlp", video_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            return {"error": "yt-dlp failed", "details": result.stderr}

        return {"status": "Download started ✅", "output": result.stdout}

    except Exception as e:
        return {"error": f"Internal crash: {str(e)}"}
