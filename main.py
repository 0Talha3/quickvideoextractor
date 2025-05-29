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
        if request.headers.get("content-type") != "application/json":
            raise HTTPException(status_code=400, detail="Content-Type must be application/json")

        data = await request.json()
        video_url = data.get("url")

        if not video_url:
            return {"error": "No video URL provided"}

        # For now, just return the URL back
        return {"status": "Key accepted!", "url": video_url}

    except Exception as e:
        return {"error": "JSON parsing failed", "details": str(e)}
