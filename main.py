from fastapi import FastAPI, Request, HTTPException
import os

app = FastAPI()  # ✅ This line defines 'app'

API_KEY = os.getenv("API_KEY")

@app.post("/download")
async def download_video(request: Request):
    client_key = request.headers.get("X-API-KEY")
    if client_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key ❌")

    data = await request.json()
    video_url = data.get("url")

    # Here you can put your yt-dlp code to download the video
    return {"status": "Download started", "url": video_url}
