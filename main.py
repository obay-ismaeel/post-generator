from pydantic import BaseModel
from llama_service import CreatePost
import whisper
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
from pathlib import Path

app = FastAPI()

model = whisper.load_model("base")

class Item(BaseModel):
    script: str
    link: str

@app.post('/api/blog')
async def generate_linkedin(item:Item):
    return await CreatePost(item.script, item.link, "blog")

@app.post('/api/linkedin')
async def generate_linkedin(item:Item):
    return await CreatePost(item.script, item.link, "linkedin")

@app.post('/api/twitter')
async def generate_linkedin(item:Item):
    return await CreatePost(item.script, item.link, "twitter")

@app.post('/api/facebook')
async def generate_linkedin(item:Item):
    return await CreatePost(item.script, item.link, "facebook")

@app.post("/api/whisper")
async def get_transcribe(file: UploadFile = File(...)):
    current_directory = Path.cwd()
    
    file_path = f"{current_directory}{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    result = model.transcribe(file_path)

    os.remove(file_path)

    transcription_text = result.get("text", "")

    return JSONResponse(content={"text": transcription_text})