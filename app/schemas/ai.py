from pydantic import BaseModel

class ChatRequest(BaseModel):
    prompt: str
    image_url: str

class ChatResponse(BaseModel):
    answer: str
    model: str
