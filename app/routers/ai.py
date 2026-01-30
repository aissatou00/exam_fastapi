
from fastapi import APIRouter, Depends
from schemas.ai import ChatRequest, ChatResponse
from fastapi import APIRouter, UploadFile, File, Form
from services.openrouter_client import analyze_image


router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/chat")
async def chat(
    prompt: str = Form(...),
    file: UploadFile = File(...)
):
    image_bytes = await file.read()
    answer = await analyze_image(prompt, image_bytes)
    return {"answer": answer}
 


 
 