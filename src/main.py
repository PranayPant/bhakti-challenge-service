import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.utils.profile import profile_async
from src.models.gemini import GeminiLLM
from src.service.auth import get_access_token


class PromptRequest(BaseModel):
    prompt: str
    model_name: str = "gemini-2.5-flash"


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Load Gemini API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable not set.")

gemini_llm = GeminiLLM(GEMINI_API_KEY)


# REST API endpoint for Gemini LLM
@app.post("/generate")
async def generate_text(request: PromptRequest):
    try:
        response, elapsed, time_taken = await profile_async(gemini_llm.generate_content, request.prompt, request.model_name)
        return {
            "response": response.text,
            "elapsed_seconds": elapsed,
            "time_taken": time_taken
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get('/get-token')
async def get_token():
    """An API endpoint that returns a temporary access token."""
    token = await get_access_token()
    # Return the token as a JSON response
    return JSONResponse(content={"access_token": token})
