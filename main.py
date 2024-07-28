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

@app.post('/blog')
async def generate_linkedin(item:Item):
    return await CreatePost(item.script, item.link, "blog")

@app.post('/linkedin')
async def generate_linkedin(item:Item):
    return await CreatePost(item.script, item.link, "linkedin")

@app.post('/twitter')
async def generate_linkedin(item:Item):
    return await CreatePost(item.script, item.link, "twitter")

@app.post('/facebook')
async def generate_linkedin(item:Item):
    return await CreatePost(item.script, item.link, "facebook")

@app.post("/api/whisper")
async def get_transcribe(file: UploadFile = File(...)):
    # Get the current working directory
    current_directory = Path.cwd()
    # # Get the current working directory
    # current_directory = os.getcwd()
    
    # Save the uploaded file to disk
    file_path = f"{current_directory}{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Transcribe the audio using Whisper
    result = model.transcribe(file_path)

    # Remove the temporary file
    os.remove(file_path)

    # Extract the text from the transcription result
    transcription_text = result.get("text", "")

    # Return the transcription text as a JSON response
    return JSONResponse(content={"text": transcription_text})