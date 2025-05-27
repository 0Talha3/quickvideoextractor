from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

app = FastAPI()

class VideoRequest(BaseModel):
    url: str

@app.post("/download")
def download_video(req: VideoRequest):
    try:
        result = subprocess.run(
            ["yt-dlp", "-g", req.url],
            capture_output=True,
            text=True
        )
        return {"video_url": result.stdout.strip()}
    except Exception as e:
        return {"error": str(e)}
