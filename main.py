import os
from fastapi import Request, HTTPException

API_KEY = os.getenv("API_KEY")
@app.post("/download")
async def download_video(request: Request):
    client_key = request.headers.get("X-API-KEY")
    if client_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key ❌")
    
    # your existing video download code here
