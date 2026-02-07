import os
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from main import run_pipeline

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
