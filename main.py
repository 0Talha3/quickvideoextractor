from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
import os
import subprocess
import uuid

app = FastAPI()

# Load the API key from Render's environment
API_KEY = os.getenv("API_KEY")

# POST route to trigger download
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

        # Generate unique filename
        video_id = str(uuid.uuid4())
        output_path = f"static/{video_id}.mp4"

        # Run yt-dlp to download video
        result = subprocess.run(
            ["yt-dlp", "-f", "best", "-o", output_path, video_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Only return error if "ERROR:" found in stderr
        if "ERROR:" in result.stderr:
            return {
                "error": "yt-dlp failed",
                "details": result.stderr
            }

        return {
            "status": "Download complete ✅",
            "file_url": f"/files/{video_id}.mp4"
        }

    except Exception as e:
        return {
            "error": "Server crash",
            "details": str(e)
        }

# Make sure the static folder exists
if not os.path.exists("static"):
    os.makedirs("static")

# Serve the downloaded videos
app.mount("/files", StaticFiles(directory="static"), name="static")
