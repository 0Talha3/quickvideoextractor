# main.py

from fastapi import FastAPI, Request, HTTPException
import os, subprocess, uuid, shutil
from fastapi.staticfiles import StaticFiles

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

        video_id = str(uuid.uuid4())
        output_path = f"static/{video_id}.mp4"

        result = subprocess.run(
            ["yt-dlp", "-f", "best", "-o", output_path, video_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            return {"error": "yt-dlp failed", "details": result.stderr}

        return {
            "status": "Download complete ✅",
            "file_url": f"/files/{video_id}.mp4"
        }

    except Exception as e:
        return {"error": f"Server crash", "details": str(e)}"

# Serve the video files
app.mount("/files", StaticFiles(directory="static"), name="static")
