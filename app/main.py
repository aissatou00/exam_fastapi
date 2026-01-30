

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import os
import shutil
from pathlib import Path
import uuid 
from routers.ai import router as ai_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="FastAPI File Upload Service")

@app.get("/ping")
def ping():
    return {"message": "pong"}


UPLOAD_DIR = Path("uploads/cvs")
UPLOAD_DIR.mkdir(exist_ok=True)
MAX_FILE_SIZE = 5*1024*1024

@app.post("/cvs/uploads")    
async def upload_cv(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=415, detail="Unspported Media TypeVar")

    contents = await file.read()
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Payload Too Large")

  
    cv_id = uuid.uuid4()
    
    file_path = f"uploads/cvs/{cv_id}.pdf"
    
     
    return {
        "id" : cv_id,
        "filename": file.filename,
    }
    
app.include_router(ai_router)
    
    

