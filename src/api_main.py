import os
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time
from main import run_pipeline
try:
    from google_meet_service import list_recent_conferences, get_transcript
except ImportError:
    list_recent_conferences = lambda: []
    get_transcript = lambda name: ""

app = FastAPI(title="AI Meeting Minutes API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Meeting Minutes API is running"}

@app.post("/process")
async def process_file(file: UploadFile = File(...)):
    """
    Process an uploaded transcript/audio file and return meeting minutes.
    """
    # Create a temporary file to save the upload
    suffix = os.path.splitext(file.filename)[1].lower()
    
    # Supported formats check
    if suffix not in [".txt", ".json", ".mp3", ".wav", ".m4a", ".mp4", ".mpeg"]:
        raise HTTPException(status_code=400, detail=f"Unsupported file format: {suffix}")

    try:
        # Create temp directory if it doesn't exist
        temp_dir = "temp_uploads"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
        temp_file_path = os.path.join(temp_dir, f"upload_{file.filename}")
        
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Run the existing pipeline in silent mode
        result = run_pipeline(temp_file_path, silent=True)

        # Cleanup temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        if result:
            return result
        else:
            raise HTTPException(status_code=500, detail="Failed to process meeting minutes.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-text")
async def process_text(data: dict):
    """
    Process a raw transcript text and return meeting minutes.
    """
    text = data.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="No transcript text provided")

    try:
        # Save text to a temporary file
        temp_dir = "temp_uploads"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
        temp_file_path = os.path.join(temp_dir, f"live_session_{int(time.time())}.txt")
        
        with open(temp_file_path, "w", encoding="utf-8") as f:
            f.write(text)

        # Run the existing pipeline in silent mode
        result = run_pipeline(temp_file_path, silent=True)

        # Cleanup temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        if result:
            return result
        else:
            raise HTTPException(status_code=500, detail="Failed to process meeting minutes.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/list-meetings")
async def list_meetings():
    """
    List recent Google Meet conferences.
    """
    try:
        conferences = list_recent_conferences()
        return {"conferences": conferences}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/fetch-meeting-transcript")
async def fetch_meeting_transcript(data: dict):
    """
    Fetch a transcript from Google Meet and generate MOM.
    """
    name = data.get("conference_name")
    if not name:
        raise HTTPException(status_code=400, detail="No conference name provided")

    try:
        text = get_transcript(name)
        if not text:
            raise HTTPException(status_code=404, detail="No transcript found or API not configured")
        
        temp_dir = "temp_uploads"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
        temp_file_path = os.path.join(temp_dir, f"meet_archive_{int(time.time())}.txt")
        with open(temp_file_path, "w", encoding="utf-8") as f:
            f.write(text)

        result = run_pipeline(temp_file_path, silent=True)
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
