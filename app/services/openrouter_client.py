import os
import httpx
import base64
from dotenv import load_dotenv
 
load_dotenv()
 
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-001")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_APP_NAME= os.getenv("OPENROUTER_APP_NAME", "cv")
OPENROUTER_SITE_URL=os.getenv("OPENROUTER_SITE_URL", "http://localhost/")
 
class OpenRouterError(RuntimeError):
    pass
 
async def analyze_image(prompt: str, image_bytes: bytes) -> str:
    if not OPENROUTER_API_KEY:
        raise OpenRouterError("OPENROUTER_API_KEY manquante dans le .env")
 
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
 
    url = f"{OPENROUTER_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": OPENROUTER_SITE_URL,
        "X-Title": OPENROUTER_APP_NAME,
    }
 
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "user",
             "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url",
                     "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                    }
                ]
            }
        ],
    }
 
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, headers=headers, json=payload)
       
    if response.status_code >= 400:
        raise OpenRouterError(f"OpenRouter error ({response.status_code}): {response.text}")
 
    data = response.json()
    return data["choices"][0]["message"]["content"]