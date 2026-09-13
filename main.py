from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import yt_dlp
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/download")
async def download_video(data: dict):
    url = data.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    
    output_path = "downloaded_video.mp4"
    
    # যদি আগের কোনো ফাইল থাকে তা ডিলিট করে দেওয়া
    if os.path.exists(output_path):
        os.remove(output_path)

    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
        'noplaylist': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        if os.path.exists(output_path):
            return {"success": True, "filename": output_path}
        else:
            raise HTTPException(status_code=500, detail="Download failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-file")
async def get_file():
    path = "downloaded_video.mp4"
    if os.path.exists(path):
        return FileResponse(path, media_type="video/mp4", filename="tiktok_video.mp4")
    raise HTTPException(status_code=404, detail="File not found")