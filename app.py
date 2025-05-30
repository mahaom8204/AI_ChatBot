from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI
import os

# Your OpenRouter API key
my_api_key = "YOUR_API_KEY"

# Setup OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=my_api_key,
)

# Initialize FastAPI app
app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change in prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the React static files (after build)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Serve index.html for root route
@app.get("/")
async def serve_index():
    return FileResponse("frontend/index.html")

# Pydantic model for incoming request
class PromptRequest(BaseModel):
    prompt: str

# Chat endpoint
@app.post("/chat")
async def chat_endpoint(req: PromptRequest):
    sys_prompt = """
    Your name is Donna from here on.

    You are a helpful assistant.
    Do not use special characters in the response like *, @, #, %, etc.
    Use only basic punctuation: period, comma, question mark, exclamation mark.
    Do not use emojis or math/code symbols.
    """

    completion = client.chat.completions.create(
        model="mistralai/devstral-small:free",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": req.prompt},
        ]
    )

    return {"response": completion.choices[0].message.content}
