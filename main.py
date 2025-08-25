

import os
import time
from datetime import timedelta
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import google.generativeai as genai


class PromptRequest(BaseModel):
    prompt: str
    model_name: str = "gemini-2.5-flash"


app = FastAPI()

# Load Gemini API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable not set.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-flash-2.5')


@app.post("/generate")
async def generate_text(request: PromptRequest):
    try:
        model = genai.GenerativeModel(request.model_name)
        start_time = time.time()
        response = model.generate_content(request.prompt)
        elapsed = time.time() - start_time
        time_taken = str(timedelta(seconds=elapsed))
        return {"response": response.text, "elapsed_seconds": elapsed, "time_taken": time_taken}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
